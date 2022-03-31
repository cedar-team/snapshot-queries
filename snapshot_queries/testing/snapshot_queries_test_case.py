import snapshottest
from contextlib import contextmanager

django_available = False
try:
    import django.conf
    import django.db
except ImportError:
    pass
else:
    django_available = True

if django_available:
    import snapshottest.django


class AssertQueriesMatchMixin:
    @contextmanager
    def assertQueriesMatchSnapshot(self):
        yield


class SnapshotQueriesTestCase(snapshottest.TestCase, AssertQueriesMatchMixin):
    pass


if django_available:
    class SnapshotQueriesDjangoTestCase(
        snapshottest.django.TestCase, AssertQueriesMatchMixin
    ):
        pass
