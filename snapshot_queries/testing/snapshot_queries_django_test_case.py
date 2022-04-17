import snapshottest.django

from .assert_queries_match_mixin import AssertQueriesMatchMixin


class SnapshotQueriesDjangoTestCase(
    AssertQueriesMatchMixin, snapshottest.django.TestCase
):
    @property
    def module(self):
        return self._snapshot.module

    @property
    def test_name(self):
        return self._snapshot.test_name
