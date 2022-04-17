import datetime
import json
import logging
from contextlib import contextmanager
from typing import Callable, Dict

from .optional_dependencies import DJANGO_INSTALLED, SQLALCHEMY_INSTALLED
from .query import Query
from .query_list import QueryList

try:
    from freezegun.api import real_time
except ImportError:
    from time import time as real_time

if SQLALCHEMY_INSTALLED:
    import sqlalchemy
    import sqlalchemy.sql


if DJANGO_INSTALLED:
    import django.conf
    import django.db


logger = logging.getLogger(__name__)


@contextmanager
def snapshot_queries():
    """Context Manager for capturing queries executed."""
    queries = QueryList()

    snapshot_queries_sqlalchemy = (
        _snapshot_queries_sqlalchemy if SQLALCHEMY_INSTALLED else _nullcontextmanager
    )

    snapshot_queries_django = (
        _snapshot_queries_django
        if (DJANGO_INSTALLED and django.conf.settings.configured)
        else _nullcontextmanager
    )

    with snapshot_queries_sqlalchemy(queries), snapshot_queries_django(queries):
        yield queries


@contextmanager
def _snapshot_queries_sqlalchemy(queries: QueryList):
    @sqlalchemy.event.listens_for(sqlalchemy.engine.Engine, "before_cursor_execute")
    def sqlalchemy_before_cursor_execute(
        conn, cursor, statement, parameters, context, executemany
    ):
        conn.info.setdefault("query_start_time", []).append(real_time())

    @sqlalchemy.event.listens_for(sqlalchemy.engine.Engine, "after_cursor_execute")
    def sqlalchemy_after_cursor_execute(
        conn, cursor, statement: str, parameters, context, executemany
    ):
        start_time = conn.info["query_start_time"].pop()
        stop_time = real_time()

        # TODO: Support paramstyles 'numeric' and 'named'
        sql = statement
        paramstyle = conn.dialect.paramstyle
        if paramstyle == "qmark":
            for param in parameters:
                sql = sql.replace("?", repr(param), 1)
        elif paramstyle in ("format", "pyformat"):
            try:
                sql = statement % parameters
            except TypeError:
                logger.error("Failed to render sql statement")

        queries.append(
            Query.create(
                idx=len(queries),
                db_type=conn.engine.name,
                db="",
                sql=sql,
                sql_parameterized=statement,
                params=parameters,
                raw_params=parameters,
                start_time=start_time,
                stop_time=stop_time,
            )
        )

    try:
        yield queries
    finally:
        sqlalchemy.event.remove(
            sqlalchemy.engine.Engine,
            "before_cursor_execute",
            sqlalchemy_before_cursor_execute,
        )

        sqlalchemy.event.remove(
            sqlalchemy.engine.Engine,
            "after_cursor_execute",
            sqlalchemy_after_cursor_execute,
        )


@contextmanager
def _snapshot_queries_django(queries: QueryList):
    initial_cursors: Dict[str, Callable] = dict()
    initial_chunked_cursors: Dict[str, Callable] = dict()

    def new_cursor(conn):
        def inner(*args, **kwargs):
            return _SnapshotQueriesDjangoCursorWrapper(
                initial_cursors[conn.alias](*args, **kwargs), queries
            )

        return inner

    def new_chunked_cursor(conn):
        def inner(*args, **kwargs):
            return _SnapshotQueriesDjangoCursorWrapper(
                initial_chunked_cursors[conn.alias](*args, **kwargs),
                queries,
            )

        return inner

    for alias in django.db.connections:
        connection = django.db.connections[alias]
        initial_cursors[alias] = connection.cursor
        initial_chunked_cursors[alias] = connection.chunked_cursor

        # monkey-patch connection.cursor and connection.chunked_cursor
        connection.cursor = new_cursor(connection)
        connection.chunked_cursor = new_chunked_cursor(connection)

    try:
        yield
    finally:
        for alias in django.db.connections:
            connection = django.db.connections[alias]
            connection.cursor = initial_cursors[alias]
            connection.chunked_cursor = initial_chunked_cursors[alias]


@contextmanager
def _nullcontextmanager(*args, **kwargs):
    yield


class _SnapshotQueriesDjangoCursorWrapper:
    def __init__(self, cursor, queries: QueryList):
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
            return django.utils.encoding.force_str(
                param, strings_only=not isinstance(param, CONVERT_TYPES)
            )
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

            _params = ""
            try:
                _params = json.dumps(self._decode(params))
            except TypeError:
                pass  # object not JSON serializable

            self._queries.append(
                Query.create(
                    idx=len(self._queries),
                    db_type=getattr(self.cursor.db, "vendor", "unknown"),
                    db=getattr(self.cursor.db, "alias", "default"),
                    sql=sql,
                    sql_parameterized=sql_parameterized,
                    params=_params,
                    raw_params=params,
                    start_time=start_time,
                    stop_time=stop_time,
                )
            )

        return results
