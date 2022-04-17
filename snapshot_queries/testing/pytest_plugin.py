import snapshot_queries.optional_dependencies

if snapshot_queries.optional_dependencies.SNAPSHOTTEST_INSTALLED:

    from contextlib import contextmanager

    from snapshottest.pytest import PyTestSnapshotTest

    from .assert_queries_match_mixin import AssertQueriesMatchMixin
    import pytest

    class PyTestSnapshotQueriesTest(PyTestSnapshotTest, AssertQueriesMatchMixin):
        @contextmanager
        def assert_queries_match(self, name=""):
            with self._assert_queries_match(name=name) as queries_executed:
                yield queries_executed

        def assert_match_snapshot(self, value, name=""):
            return self.assert_match(value, name)

    @pytest.fixture
    def queries_snapshot(request):
        with PyTestSnapshotQueriesTest(request) as snapshot_test:
            yield snapshot_test