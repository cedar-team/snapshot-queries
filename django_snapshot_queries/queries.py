import collections
import sys
from typing import Dict, Callable
from collections import UserDict

from .timedelta import TimeDelta

from .query import Query
from .sliceable_list import SliceableList


class Queries(SliceableList):
    """List Query instances."""

    def __str__(self):
        return self.display_string()

    def diff(self, other: "Queries"):
        # TODO: Figure out what this should return
        raise NotImplementedError

    def display(
        self,
        *,
        code: bool = False,
        duration: bool = False,
        idx: bool = False,
        location: bool = False,
        stacktrace: bool = False,
        sql=False,
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
            )
            + "\n"
        )

    def display_string(
        self,
        *,
        code: bool = False,
        duration: bool = False,
        idx: bool = False,
        location: bool = False,
        stacktrace: bool = False,
        sql=False,
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
            )
            string += f"Query {i}\n"
            string += "---------\n"
            string += f"{query_string}\n\n\n"
        return string.rstrip()

    def duplicates(self) -> "DuplicateQueries":
        """Return duplicate queries."""
        queries_by_sql: Dict[str, Queries] = collections.defaultdict(Queries)
        for query in self:
            queries_by_sql[query.sql].append(query)

        dupes = DuplicateQueries()
        for sql, queries in queries_by_sql.items():
            if len(queries) > 1:
                dupes[sql] = queries

        return dupes

    @property
    def duration(self) -> int:
        """Return duration of queries."""
        return sum((q.duration for q in self), TimeDelta())

    def order_by(self, field: str) -> "Queries":
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

    def similar(self) -> "SimilarQueries":
        """Return similar queries."""
        queries = collections.defaultdict(Queries)
        for query in self:
            queries[query.sql_parameterized].append(query)

        similar = SimilarQueries()
        for sql, queries in queries.items():
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


class DuplicateQueries(UserDict):
    def __str__(self):
        return self.display_string()

    def display(
        self,
        *,
        code: bool = False,
        duration: bool = False,
        idx: bool = False,
        location: bool = False,
        stacktrace: bool = False,
        sql=False,
    ):
        sys.stdout.write(
            self.display_string(
                code=code,
                duration=duration,
                idx=idx,
                location=location,
                stacktrace=stacktrace,
                sql=sql,
            )
            + "\n"
        )

    def display_string(
        self,
        *,
        code: bool = False,
        duration: bool = False,
        idx: bool = False,
        location: bool = False,
        stacktrace: bool = False,
        sql: bool = False,
    ) -> str:
        string = ""
        for queries in self.values():

            queries: Queries
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
            )

        return string


class SimilarQueries(DuplicateQueries):
    def display_string(
        self,
        *,
        code: bool = False,
        duration: bool = False,
        idx: bool = False,
        location: bool = False,
        stacktrace: bool = False,
        sql: bool = False,
    ) -> str:
        string = ""
        for queries in self.values():

            queries: Queries
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
            )

        return string
