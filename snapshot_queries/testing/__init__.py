# flake8: noqa
import snapshot_queries.optional_dependencies

if snapshot_queries.optional_dependencies.SNAPSHOTTEST_INSTALLED:
    from .snapshot_queries_test_case import SnapshotQueriesTestCase

    __all__ = ["SnapshotQueriesTestCase"]

    if snapshot_queries.optional_dependencies.DJANGO_INSTALLED:
        from .snapshot_queries_django_test_case import SnapshotQueriesDjangoTestCase  # noqa

        __all__.append("SnapshotQueriesDjangoTestCase")
