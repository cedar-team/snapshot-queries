import collections
import sys
from collections import UserDict
from typing import Callable, Dict

from .query import Query
from .sliceable_list import SliceableList
from .timedelta import TimeDelta


class QueryList(SliceableList):
    """List of Query instances."""

    def __str__(self):
        return self.display_string()

    def diff(self, other: "QueryList"):
        # TODO: Figure out what this should return
        raise NotImplementedError

    def display(
        self,
        *,
        code: bool = True,
        duration: bool = True,
        idx: bool = False,
        location: bool = True,
        stacktrace: bool = False,
        sql=True,
        colored=True,
        formatted=True,
    ):
        """
        Display info about each query.

        Supported attributes to display:
            - code (the python code that triggered the query)
            - duration (how long the query took to execute)
            - idx (the index of the query executed)
            - location  (the location in our code where the query was executed)
            - stacktrace (the full stacktrace for each query)
            - sql (the sql statement of the query)

        If no attributes are specified then the code, line number, duration, and sql
        statement are displayed.
        """
        sys.stdout.write(
            self.display_string(
                code=code,
                duration=duration,
                idx=idx,
                location=location,
                stacktrace=stacktrace,
                sql=sql,
                colored=colored,
                formatted=formatted,
            )
            + "\n"
        )

    def display_string(
        self,
        *,
        code: bool = True,
        duration: bool = True,
        idx: bool = False,
        location: bool = True,
        stacktrace: bool = False,
        sql=True,
        colored=True,
        formatted=True,
    ) -> str:
        string = ""
        for i, query in enumerate(self, start=1):
            query_string = query.display_string(
                code=code,
                duration=duration,
                idx=idx,
                location=location,
                stacktrace=stacktrace,
                sql=sql,
                colored=colored,
                formatted=formatted,
            )
            string += f"Query {i}\n"
            string += "---------\n"
            string += f"{query_string}\n\n\n"
        return string.rstrip()

    def duplicates(self) -> "DuplicateQueryList":
        """Return duplicate queries."""
        queries_by_sql: Dict[str, QueryList] = collections.defaultdict(QueryList)
        for query in self:
            queries_by_sql[query.sql].append(query)

        dupes = DuplicateQueryList()
        for sql, queries in queries_by_sql.items():
            if len(queries) > 1:
                dupes[sql] = queries

        return dupes

    def total_duration(self) -> int:
        """Return duration of queries."""
        return sum((q.duration for q in self), TimeDelta())

    def order_by(self, field: str) -> "QueryList":
        """
        Order queries by field.

        Supported fields:
            duration
            idx
            location

        Allows sorting in reverse order by prepending '-':

            slowest_queries = queries.order_by('-duration')[:5]
        """
        reverse = True if field.startswith("-") else False

        keys: Dict[str, Callable] = dict(
            duration=self._order_by_duration_key,
            location=self._order_by_location_key,
            idx=self._order_by_idx_key,
        )

        field = field.strip("-+")
        key = keys.get(field)

        self.sort(key=key, reverse=reverse)
        return self

    def similar(self) -> "SimilarQueryList":
        """Return similar queries."""
        queries_by_sql: Dict[str, QueryList] = collections.defaultdict(QueryList)
        for query in self:
            queries_by_sql[query.sql_parameterized].append(query)

        similar = SimilarQueryList()
        for sql, queries in queries_by_sql.items():
            if len(queries) > 1:
                similar[sql] = queries

        return similar

    @staticmethod
    def _order_by_duration_key(query: Query) -> TimeDelta:
        return query.duration

    @staticmethod
    def _order_by_idx_key(query: Query) -> int:
        return query.idx

    @staticmethod
    def _order_by_location_key(query: Query) -> str:
        return query.location


class DuplicateQueryList(UserDict):
    def __str__(self):
        return self.display_string()

    def display(
        self,
        *,
        code: bool = True,
        duration: bool = True,
        idx: bool = False,
        location: bool = True,
        stacktrace: bool = False,
        sql=True,
        colored=True,
        formatted=True,
    ):
        sys.stdout.write(
            self.display_string(
                code=code,
                duration=duration,
                idx=idx,
                location=location,
                stacktrace=stacktrace,
                sql=sql,
                colored=colored,
                formatted=formatted,
            )
            + "\n"
        )

    def display_string(
        self,
        *,
        code: bool = True,
        duration: bool = True,
        idx: bool = False,
        location: bool = True,
        stacktrace: bool = False,
        sql=True,
        colored=True,
        formatted=True,
    ) -> str:
        string = ""
        for queries in self.values():

            string += (
                f"\n\n============================\n"
                f"{len(queries)} duplicate queries detected\n"
                f"============================\n"
            )
            string += queries.display_string(
                code=code,
                duration=duration,
                idx=idx,
                location=location,
                stacktrace=stacktrace,
                sql=sql,
                colored=colored,
                formatted=formatted,
            )

        return string


class SimilarQueryList(DuplicateQueryList):
    def display_string(
        self,
        *,
        code: bool = True,
        duration: bool = True,
        idx: bool = False,
        location: bool = True,
        stacktrace: bool = False,
        sql=True,
        colored=True,
        formatted=True,
    ) -> str:
        string = ""
        for queries in self.values():
            string += (
                f"\n\n==========================\n"
                f"{len(queries)} similar queries detected\n"
                f"==========================\n"
            )
            string += queries.display_string(
                code=code,
                duration=duration,
                idx=idx,
                location=location,
                stacktrace=stacktrace,
                sql=sql,
                colored=colored,
                formatted=formatted,
            )

        return string
