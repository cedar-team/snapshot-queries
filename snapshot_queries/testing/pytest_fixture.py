from snapshottest.pytest import PyTestSnapshotTest
from snapshot_queries import snapshot_queries


class PyTestSnapshotQueriesTest(PyTestSnapshotTest):

    def assert_queries_match(self, name=""):
        yield
