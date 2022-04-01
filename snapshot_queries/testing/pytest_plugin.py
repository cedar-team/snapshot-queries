from snapshottest.pytest import PyTestSnapshotTest
from snapshot_queries import snapshot_queries
from .snapshot_queries_test_case import AssertQueriesMatchMixin
from contextlib import contextmanager

pytest_installed = True
try:
    import pytest
except Exception:
    pytest_installed = False


class PyTestSnapshotQueriesTest(PyTestSnapshotTest, AssertQueriesMatchMixin):
    @contextmanager
    def assert_queries_match(self, name=""):
        with self._assert_queries_match(name=name):
            yield

    def assert_match_snapshot(self, value, name=""):
        self.assert_match(value, name)


if pytest_installed:

    @pytest.fixture
    def snapshot_queries_fixture(request):
        with PyTestSnapshotQueriesTest(request) as snapshot_test:
            yield snapshot_test
