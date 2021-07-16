import datetime
import json

from django.db import connections
from django.utils.encoding import force_text

from .timedelta import TimeDelta

from .queries import Queries
from .query import Query
from .stacktrace import StackTrace
from contextlib import contextmanager

try:
    from freezegun.api import real_time
except ImportError:
    from time import time as real_time

sql_alchemy_available = False
try:
    import sqlalchemy

    sql_alchemy_available = True
except ImportError:
    pass
else:
    from sqlalchemy import event
    from sqlalchemy.engine import Engine


django_available = False
try:
    import django
except ImportError:
    pass
else:
    from django.db import connections
    from django.utils.encoding import force_text

    django_available = True


@contextmanager
def snapshot_queries():
    """
    Context Manager for debugging queries executed.

    Usage:

        from api_app.models import Provider, User
        with snapshot_queries() as queries:
            User.objects.only('protected_id').get(id=1)
            User.objects.only('protected_id').get(id=1)
            User.objects.only('protected_id').get(id=7)
            Provider.objects.only('name').get(id=1)
            Provider.objects.only('name').get(id=1)
            Provider.objects.only('name').get(id=5)

        # Display the queries that were executed
        queries.display()

        # Display the stacktrace, sql, and duration of each query
        queries.display(stacktrace=True, sql=True, duration=True)

        # Display only the sql
        queries.display(sql=True)

        # Display the code executed, the line number, and the sql of each query
        queries.display(code=True, location=True, sql=True)

        # Order queries by duration
        fastest_queries = queries.order_by('duration')[:3]
        slowest_queries = queries.order_by('-duration')[:3]

        # Inspect a specific query
        slowest_query = queries.order_by('-duration')[0]
        slowest_query.display(code=True, location=True, sql=True)

        # Display queries with identical sql statements together
        duplicates = queries.duplicates().display()

        # Display queries with similar sql statements
        sim = queries.similar().display()
    """
    queries = Queries()

    snapshot_queries_sqlalchemy = (
        _snapshot_queries_sqlalchemy if sql_alchemy_available else _nullcontextmanager
    )

    snapshot_queries_django = (
        _snapshot_queries_sqlalchemy if sql_alchemy_available else _nullcontextmanager
    )

    with snapshot_queries_sqlalchemy(queries), snapshot_queries_django(queries):
        yield


@contextmanager
def _snapshot_queries_sqlalchemy(queries: Queries):
    @event.listens_for(Engine, "before_cursor_execute")
    def sqlalchemy_before_cursor_execute(
        conn, cursor, statement, parameters, context, executemany
    ):
        conn.info.setdefault("query_start_time", []).append(real_time())

    @event.listens_for(Engine, "after_cursor_execute")
    def sqlalchemy_after_cursor_execute(
        conn, cursor, statement, parameters, context, executemany
    ):
        start_time = conn.info["query_start_time"].pop()
        stop_time = real_time()
        sql = statement % parameters
        stacktrace = StackTrace.load()

        queries.append(
            Query(
                idx=len(queries),
                db_type=conn.engine.name,
                db="",  # TODO: Figure out if it's possible to get the db name
                sql=sql,
                sql_parameterized=statement,
                duration=TimeDelta(seconds=(stop_time - start_time)),
                params=parameters,
                raw_params=parameters,
                stacktrace=stacktrace,
                start_time=start_time,
                stop_time=stop_time,
                is_select=sql.lower().strip().startswith("select"),
            )
        )

    event.remove(
        Engine,
        "before_cursor_execute",
        sqlalchemy_before_cursor_execute,
    )

    event.remove(
        Engine,
        "after_cursor_execute",
        sqlalchemy_after_cursor_execute,
    )

    yield

    event.remove(
        Engine,
        "before_cursor_execute",
        sqlalchemy_before_cursor_execute,
    )

    event.remove(
        Engine,
        "after_cursor_execute",
        sqlalchemy_after_cursor_execute,
    )


@contextmanager
def _snapshot_queries_django(queries: Queries):
    initial_cursors = dict()
    initial_chunked_cursors = dict()

    def new_cursor(conn):
        def inner(*args, **kwargs):
            return _DebugQueriesCursorWrapper(
                initial_cursors[conn.alias](*args, **kwargs), queries
            )

        return inner

    def new_chunked_cursor(conn):
        def inner(*args, **kwargs):
            return _DebugQueriesCursorWrapper(
                initial_chunked_cursors[conn.alias](*args, **kwargs),
                queries,
            )

        return inner

    for alias in connections:
        connection = connections[alias]
        initial_cursors[alias] = connection.cursor
        initial_chunked_cursors[alias] = connection.chunked_cursor

        # monkey-patch connection.cursor and connection.chunked_cursor
        connection.cursor = new_cursor(connection)
        connection.chunked_cursor = new_chunked_cursor(connection)

    yield

class _DebugQueriesCursorWrapper:
    def __init__(self, cursor, queries: Queries):
        self.cursor = cursor
        self._queries = queries

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def __getattr__(self, attr):
        return getattr(self.cursor, attr)

    def __iter__(self):
        return iter(self.cursor)

    def callproc(self, procname, params=None):
        return self._record(method=self.cursor.callproc, sql=procname, params=params)

    def execute(self, sql, params=None):
        return self._record(method=self.cursor.execute, sql=sql, params=params)

    def executemany(self, sql, param_list):
        return self._record(method=self.cursor.executemany, sql=sql, params=param_list)

    def _decode(self, param):
        # If a sequence type, decode each element separately
        if isinstance(param, (tuple, list)):
            return [self._decode(element) for element in param]

        # If a dictionary type, decode each value separately
        if isinstance(param, dict):
            return {key: self._decode(value) for key, value in param.items()}

        # make sure datetime, date and time are converted to string by force_text
        CONVERT_TYPES = (datetime.datetime, datetime.date, datetime.time)
        try:
            return force_text(param, strings_only=not isinstance(param, CONVERT_TYPES))
        except UnicodeDecodeError:
            return "(encoded string)"

    def _quote_expr(self, element):
        if isinstance(element, str):
            return "'%s'" % element.replace("'", "''")
        else:
            return repr(element)

    def _quote_params(self, params):
        if not params:
            return params
        if isinstance(params, dict):
            return {key: self._quote_expr(value) for key, value in params.items()}
        return [self._quote_expr(p) for p in params]

    def _record(self, method, sql, params):
        start_time = real_time()
        try:
            results = method(sql, params)
        finally:
            stop_time = real_time()
            duration = TimeDelta(seconds=(stop_time - start_time))
            stacktrace = StackTrace.load()
            _params = ""
            try:
                _params = json.dumps(self._decode(params))
            except TypeError:
                pass  # object not JSON serializable

            db = getattr(self.cursor.db, "alias", "default")
            db_type = getattr(self.cursor.db, "vendor", "unknown")

            # Sql might be an object (such as psycopg Composed).
            # For logging purposes, make sure it's str.
            if isinstance(sql, bytes):
                sql_parameterized = sql.decode()
            elif isinstance(sql, str):
                sql_parameterized = sql
            else:
                sql_parameterized = sql.as_string(self.cursor.connection)
            sql = self.cursor.db.ops.last_executed_query(
                self.cursor, sql, self._quote_params(params)
            )

            self._queries.append(
                Query(
                    idx=len(self._queries),
                    db_type=db_type,
                    db=db,
                    sql=sql,
                    sql_parameterized=sql_parameterized,
                    duration=duration,
                    params=_params,
                    raw_params=params,
                    stacktrace=stacktrace,
                    start_time=start_time,
                    stop_time=stop_time,
                    is_select=sql.lower().strip().startswith("select"),
                )
            )
        return results


@contextmanager
def _nullcontextmanager(*args, **kwargs):
    yield

SnapshotQueries = snapshot_queries
