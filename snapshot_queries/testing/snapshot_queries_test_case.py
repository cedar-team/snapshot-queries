import snapshottest
from contextlib import contextmanager
from snapshot_queries import snapshot_queries
import sqlparse
from typing import Tuple
import re

django_available = False
try:
    import django
except ImportError:
    pass
else:
    django_available = True

if django_available:
    import snapshottest.django


def _lcslen(x, y):
    """Build a matrix of LCS length.
    This matrix will be used later to backtrack the real LCS.
    """

    # This is our matrix comprised of list of lists.
    # We allocate extra row and column with zeroes for the base case of empty
    # sequence. Extra row and column is appended to the end and exploit
    # Python's ability of negative indices: x[-1] is the last elem.
    c = [[0 for _ in range(len(y) + 1)] for _ in range(len(x) + 1)]

    for i, xi in enumerate(x):
        for j, yj in enumerate(y):
            if xi == yj:
                c[i][j] = 1 + c[i - 1][j - 1]
            else:
                c[i][j] = max(c[i][j - 1], c[i - 1][j])
    return c


def backtrack(c, x, y, i, j):
    """Backtrack the LCS length matrix to get the actual LCS"""
    if i == -1 or j == -1:
        return ""
    elif x[i] == y[j]:
        return backtrack(c, x, y, i - 1, j - 1) + x[i]
    elif c[i][j - 1] >= c[i - 1][j]:
        return backtrack(c, x, y, i, j - 1)
    elif c[i][j - 1] < c[i - 1][j]:
        return backtrack(c, x, y, i - 1, j)


def _calc_diff(c, x, y, i, j):
    """Print the diff using LCS length matrix by backtracking it"""

    added = []
    removed = []
    if i < 0 and j < 0:
        return added, removed
    elif i < 0:
        sub_added, sub_removed = _calc_diff(c, x, y, i, j - 1)
        added += sub_added
        removed += sub_removed
        added.append((j, y[j]))
    elif j < 0:
        sub_added, sub_removed = _calc_diff(c, x, y, i - 1, j)
        added += sub_added
        removed += sub_removed
        removed.append((i, x[i]))
    elif x[i] == y[j]:
        sub_added, sub_removed = _calc_diff(c, x, y, i - 1, j - 1)
        added += sub_added
        removed += sub_removed
        return added, removed
    elif c[i][j - 1] >= c[i - 1][j]:
        sub_added, sub_removed = _calc_diff(c, x, y, i, j - 1)
        added += sub_added
        removed += sub_removed
        added.append((j, y[j]))
    elif c[i][j - 1] < c[i - 1][j]:
        sub_added, sub_removed = _calc_diff(c, x, y, i - 1, j)
        added += sub_added
        removed += sub_removed
        removed.append((i, x[i]))

    return added, removed


def diff_lists_detailed(x: list, y: list) -> Tuple[list, list]:
    """
    Diff 2 lists and get added and removed with indexes. This use an LCS algo described here.
    https://en.wikipedia.org/wiki/Longest_common_subsequence_problem


    This is not necessary in most cases. You can use

    `added = set(x) - set(y); removed = set(y) - set(x)` works in most cases

    """
    c = _lcslen(x, y)
    return _calc_diff(c, x, y, len(x) - 1, len(y) - 1)


def filter_query(query):
    # Exclude SAVEPOINT and any query on `django_content_type` that does NOT involve a
    # join. The content type queries are unpredictable due to Django's caching and
    # often cause flakiness in tests.
    return "SAVEPOINT" not in query and (
        "JOIN" in query or "django_content_type" not in query
    )


def change_query(query):
    flags = re.IGNORECASE | re.DOTALL
    query = re.sub(
        r"SELECT[\s\n](.*?)[\s\n]FROM", "SELECT ... FROM", query, flags=flags
    )
    query = re.sub(
        r"UPDATE[\s\n](.*?)[\s\\n]SET.+", r"UPDATE \1 SET ...", query, flags=flags
    )
    query = re.sub(
        r"INSERT INTO[\s\n](.*?)[\s\n]\(.*?\)",
        r"INSERT INTO \1 (...)",
        query,
        flags=flags,
    )
    # collapses snippets like `VALUES (%s, %s), (%s, %s)` to `VALUES (...)`
    query = re.sub(
        r"[(\s]VALUES\s(\((\S+(,\s+)?)+\)(,\s+)?)+",
        r" VALUES (...)",
        query,
        flags=flags,
    )
    query = re.sub(r"[\s\n]staging_\S+", r" staging_...", query, flags=flags)
    query = re.sub(r'"loading_\S+"', r'"loading_..."', query, flags=flags)
    query = re.sub(r" IN \(%s.*?\)", r" IN (...)", query, flags=flags)
    return query


class AssertQueriesMatchMixin:
    @contextmanager
    def assertQueriesMatchSnapshot(self, name: str = ""):
        """
        Assert queries matches snapshot.
        Example:
            class UnittestExample(SnapshotTestCase)
                def test_foo(self):
                    with self.assertQueriesMatchSnapshot():
                        User.objects.filter(email="something@test.com")
        """
        with self._assert_queries_match(name=name):
            yield

    @contextmanager
    def _assert_queries_match(self, name: str):
        with snapshot_queries() as queries:
            yield queries

        filtered_queries = [
            query for query in queries if filter_query(query.sql_parameterized)
        ]
        formatted_queries = [
            sqlparse.format(change_query(query.sql_parameterized), reindent=True)
            for query in filtered_queries
        ]

        two_newlines = "\n\n"
        try:
            return self.assert_match_snapshot(
                f"\n{len(formatted_queries)} Queries{two_newlines}{two_newlines.join(formatted_queries)}\n",
                name=name,
            )
        except AssertionError:
            # Catch the error and make the error more useful
            # remove trailing newlines
            prev_snapshot = self.module[self.test_name].strip()
            # Skip the "x Queries" line and split on separator
            previous_queries = [q for q in prev_snapshot.split(two_newlines)][1:]

            added, removed = diff_lists_detailed(previous_queries, formatted_queries)

            message_lines = []

            if added:
                added_strs = []
                for i, added_query in added:
                    # default to display the entire stacktrace
                    stack_trace_start_idx = 0
                    # iterate through stacktrace in reverse, stop when unittest/ is in the path
                    for idx in range(len(filtered_queries[i].stacktrace) - 1, -1, -1):
                        if "unittest/" in filtered_queries[i].stacktrace[idx].path:
                            # start from the first line after unittest/ is found
                            stack_trace_start_idx = idx + 1
                            break

                    truncated_stacktrace = filtered_queries[i].stacktrace[
                        stack_trace_start_idx:
                    ]
                    added_strs.append(
                        f"{truncated_stacktrace}{two_newlines}{added_query}"
                    )

                message_lines.extend(
                    [
                        "\n============Added Queries============",
                        "\n\n\n".join(added_strs),
                    ]
                )

            if removed:
                message_lines.extend(
                    [
                        "\n==========Removed Queries============",
                        two_newlines.join(query for _, query in removed),
                    ]
                )

        # Throw the error after the try/except so the previous message is not shown
        raise AssertionError("\n".join(message_lines))


class SnapshotQueriesTestCase(snapshottest.TestCase, AssertQueriesMatchMixin):
    @property
    def module(self):
        return self._snapshot.module

    @property
    def test_name(self):
        return self._snapshot.test_name


if django_available:

    class SnapshotQueriesDjangoTestCase(
        snapshottest.django.TestCase, AssertQueriesMatchMixin
    ):
        @property
        def module(self):
            return self._snapshot.module

        @property
        def test_name(self):
            return self._snapshot.test_name
