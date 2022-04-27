# flake8: noqa
import snapshot_queries.optional_dependencies

from .snapshot_queries_test_case import SnapshotQueriesTestCase

__all__ = ["SnapshotQueriesTestCase"]

if snapshot_queries.optional_dependencies.DJANGO_INSTALLED:
    pass

    __all__.append("SnapshotQueriesDjangoTestCase")
