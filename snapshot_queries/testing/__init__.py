from .snapshot_queries_test_case import SnapshotQueriesTestCase

django_available = False
try:
    import django.conf
    import django.db
except ImportError:
    pass
else:
    django_available = True

if django_available:
    from .snapshot_queries_test_case import SnapshotQueriesDjangoTestCase
