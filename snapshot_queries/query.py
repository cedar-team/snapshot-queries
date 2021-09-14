import sys
import typing

import attr
import sqlparse
from pygments import highlight
from pygments.formatters import TerminalFormatter
from pygments.lexers import PostgresLexer, Python3Lexer, SqlLexer

from .timedelta import TimeDelta

from .stacktrace import StackTrace, StacktraceLine


@attr.s(auto_attribs=True, repr=False)
class Query:
    db: str
    duration: TimeDelta
    idx: int
    is_select: bool
    params: str
    raw_params: typing.Tuple
    sql: str
    sql_parameterized: str
    stacktrace: StackTrace
    start_time: int
    stop_time: int
    db_type: str
    """Executed query."""

    def __repr__(self) -> str:
        truncated_sql = repr(self.sql)[:30].strip("'")
        return (
            f"Query("
            f"idx={self.idx}, "
            f"code='{self.code}', "
            f"duration={repr(self.duration)}, "
            f"location='{self.location}', "
            f"sql='{truncated_sql}...')"
        )

    def __str__(self) -> str:
        return self.display_string()

    @property
    def code(self) -> str:
        return self._last_executed_line().code

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
    ):
        sys.stdout.write(
            self.display_string(
                code=code,
                duration=duration,
                idx=idx,
                location=location,
                sql=sql,
                stacktrace=stacktrace,
                colored=colored,
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
    ) -> str:
        attributes = []

        if idx:
            attributes.append(f"index: {self.idx}")

        if duration:
            attributes.append(self.duration.humanize())

        if location:
            attributes.append(self.location)

        if code:
            attributes.append(self._formatted_code() if colored else self.code)

        if stacktrace:
            attributes.append(str(self.stacktrace))

        if sql:
            attributes.append(self._sql_str() if colored else self.sql)

        attributes = [c.strip() for c in attributes]
        return "\n\n".join(attributes).rstrip()

    @property
    def location(self) -> str:
        return self._last_executed_line().location()

    def _formatted_code(self) -> str:
        return highlight(f"{self.code}", Python3Lexer(), TerminalFormatter())

    def _formatted_sql(self) -> str:
        return sqlparse.format(self.sql, reindent=True)

    def _last_executed_line(self) -> StacktraceLine:
        last_executed_line: StacktraceLine = (
            self.stacktrace[-1] if self.stacktrace else StacktraceLine.null()
        )
        return last_executed_line

    def _sql_str(self) -> str:
        lexer = SqlLexer()

        # TODO: Handle other db_types?
        if self.db_type.lower() == "postgresql":
            lexer = PostgresLexer()

        colored_sql: str = highlight(
            f"{self._formatted_sql()}", lexer, TerminalFormatter()
        )

        return colored_sql
