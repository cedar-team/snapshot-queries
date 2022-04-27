from django.contrib.auth import get_user_model

from snapshot_queries.testing import SnapshotQueriesDjangoTestCase

User = get_user_model()


class SnapshotQueriesTest(SnapshotQueriesDjangoTestCase):
    maxDiff = None

    def test_single_query_display_string(self):
        with self.assertQueriesMatchSnapshot():
            # Use list to trigger query
            list(User.objects.only("email").filter(id=1))

    def test_multiple_queries_display_string(self):
        with self.assertQueriesMatchSnapshot():
            # Use list to trigger query
            list(User.objects.only("id").filter(id=2))
            list(User.objects.only("email").filter(id=1))

    def test_multiple_queries_duplicates(self):
        with self.assertQueriesMatchSnapshot():
            # Use list to trigger query
            # First 2 should be duplicates, not the last one
            list(User.objects.only("id").filter(id=1))
            list(User.objects.only("id").filter(id=1))
            list(User.objects.only("id").filter(id=2))

    def test_multiple_queries_similar(self):
        with self.assertQueriesMatchSnapshot():
            # Use list to trigger query
            # Second 2 should be similar, not the first because it's a different field
            list(User.objects.only("id").filter(id=1))
            list(User.objects.only("email").filter(id=1))
            list(User.objects.only("email").filter(id=2))
