import snapshot_queries.optional_dependencies

if snapshot_queries.optional_dependencies.SNAPSHOTTEST_INSTALLED:

    from contextlib import contextmanager

    import pytest
    from snapshottest.pytest import PyTestSnapshotTest

    from .assert_queries_match_mixin import AssertQueriesMatchMixin

    class PyTestQueriesSnapshotTest(PyTestSnapshotTest, AssertQueriesMatchMixin):
        @contextmanager
        def assert_match(self, name="", query_filter=None, query_rewrite=None):
            with self._assert_queries_match(
                name=name, query_filter=query_filter, query_rewrite=query_rewrite
            ) as queries_executed:
                yield queries_executed

        def assert_match_snapshot(self, value, name=""):
            return self.assert_match(value, name)

    @pytest.fixture
    def queries_snapshot(request):
        with PyTestQueriesSnapshotTest(request) as snapshot_test:
            yield snapshot_test
