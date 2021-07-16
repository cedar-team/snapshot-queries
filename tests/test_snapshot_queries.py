from django_snapshot_queries import SnapshotQueries
from django.contrib.auth import get_user_model
from snapshottest.django import TestCase

User = get_user_model()


class SnapshotQueriesTest(TestCase):
    maxDiff = None

    def test_single_query_display_string(self):
        with SnapshotQueries() as queries:
            # Use list to trigger query
            list(User.objects.only("email").filter(id=1))

        self.assertMatchSnapshot(
            queries.display_string()
        )

    def test_multiple_queries_display_string(self):
        with SnapshotQueries() as queries:
            # Use list to trigger query
            list(User.objects.only("id").filter(id=2))
            list(User.objects.only("email").filter(id=1))

        self.assertMatchSnapshot(
            queries.display_string()
        )

    def test_multiple_queries_duplicates(self):
        with SnapshotQueries() as queries:
            # Use list to trigger query
            # First 2 should be duplicates, not the last one
            list(User.objects.only("id").filter(id=1))
            list(User.objects.only("id").filter(id=1))
            list(User.objects.only("id").filter(id=2))

        self.assertMatchSnapshot(
            queries.duplicates().display_string()
        )

    def test_multiple_queries_similar(self):
        with SnapshotQueries() as queries:
            # Use list to trigger query
            # Second 2 should be similar, not the first because it's a different field
            list(User.objects.only("id").filter(id=1))
            list(User.objects.only("email").filter(id=1))
            list(User.objects.only("email").filter(id=2))

        self.assertMatchSnapshot(
            queries.similar().display_string()
        )

    def test_multiple_queries_similar(self):
        with SnapshotQueries() as queries:
            # Use list to trigger query
            # Second 2 should be similar, not the first because it's a different field
            list(User.objects.only("id").filter(id=1))
            list(User.objects.only("email").filter(id=1))
            list(User.objects.only("email").filter(id=2))

        self.assertMatchSnapshot(
            queries.similar().display_string()
        )
