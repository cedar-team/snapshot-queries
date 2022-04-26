import sys
import typing

import attr
import sqlparse
from pygments import highlight
from pygments.formatters import TerminalFormatter
from pygments.lexers import PostgresLexer, Python3Lexer, SqlLexer

from .stacktrace import StackTrace, StacktraceLine
from .timedelta import TimeDelta


@attr.s(auto_attribs=True, repr=False)
class Query:
    """Executed query."""

    code: str
    db: str
    duration: TimeDelta
    idx: int
    is_select: bool
    location: str
    params: str
    raw_params: typing.Tuple
    sql: str
    sql_parameterized: str
    stacktrace: StackTrace
    start_time: int
    stop_time: int
    db_type: str

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

    @classmethod
    def create(
        cls,
        db: str,
        idx: int,
        params: str,
        raw_params: typing.Tuple,
        sql: str,
        sql_parameterized: str,
        start_time: int,
        stop_time: int,
        db_type: str,
    ) -> "Query":
        stacktrace = StackTrace.load()

        last_executed_line: StacktraceLine = (
            stacktrace[-1] if stacktrace else StacktraceLine.null()
        )

        return cls(
            code=last_executed_line.code,
            db=db,
            duration=TimeDelta(seconds=(stop_time - start_time)),
            idx=idx,
            is_select=sql.lower().strip().startswith("select"),
            location=last_executed_line.location(),
            params=params,
            raw_params=raw_params,
            sql=sql,
            sql_parameterized=sql_parameterized,
            stacktrace=stacktrace,
            start_time=start_time,
            stop_time=stop_time,
            db_type=db_type,
        )

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
                sql=sql,
                stacktrace=stacktrace,
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
        attributes = []

        if idx:
            attributes.append(f"index: {self.idx}")

        if duration:
            attributes.append(self.duration.humanize())

        if location and self.location:
            attributes.append(self.location)

        if code:
            attributes.append(
                highlight(f"{self.code}", Python3Lexer(), TerminalFormatter())
                if (colored and formatted)
                else self.code
            )

        if stacktrace:
            attributes.append(str(self.stacktrace))

        if sql:
            attributes.append(self._enhanced_sql(colored=colored, formatted=formatted))

        attributes = [c.strip() for c in attributes]
        return "\n\n".join(attributes).rstrip()

    def _enhanced_sql(self, *, formatted: bool, colored: bool) -> str:
        sql = self.sql

        if formatted:
            sql = sqlparse.format(self.sql, reindent=True)

        if colored:
            lexer = SqlLexer()
            # TODO: Handle other db_types?
            if self.db_type.lower() == "postgresql":
                lexer = PostgresLexer()

            sql = highlight(f"{sql}", lexer, TerminalFormatter())

        return sql
