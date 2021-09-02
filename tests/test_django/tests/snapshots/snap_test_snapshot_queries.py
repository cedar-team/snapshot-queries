# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['SnapshotQueriesTest::test_multiple_queries_display_string 1'] = '''Query 1
---------
< 1 ms

/python/tests/test_django/tests/test_snapshot_queries.py:21 in test_multiple_queries_display_string

\x1b[36mlist\x1b[39;49;00m(User.objects.only(\x1b[33m"\x1b[39;49;00m\x1b[33mid\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m).filter(\x1b[36mid\x1b[39;49;00m=\x1b[34m2\x1b[39;49;00m))

\x1b[34mSELECT\x1b[39;49;00m \x1b[33m"auth_user"\x1b[39;49;00m.\x1b[33m"id"\x1b[39;49;00m
\x1b[34mFROM\x1b[39;49;00m \x1b[33m"auth_user"\x1b[39;49;00m
\x1b[34mWHERE\x1b[39;49;00m \x1b[33m"auth_user"\x1b[39;49;00m.\x1b[33m"id"\x1b[39;49;00m = \x1b[33m\'2\'\x1b[39;49;00m


Query 2
---------
< 1 ms

/python/tests/test_django/tests/test_snapshot_queries.py:22 in test_multiple_queries_display_string

\x1b[36mlist\x1b[39;49;00m(User.objects.only(\x1b[33m"\x1b[39;49;00m\x1b[33memail\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m).filter(\x1b[36mid\x1b[39;49;00m=\x1b[34m1\x1b[39;49;00m))

\x1b[34mSELECT\x1b[39;49;00m \x1b[33m"auth_user"\x1b[39;49;00m.\x1b[33m"id"\x1b[39;49;00m,
       \x1b[33m"auth_user"\x1b[39;49;00m.\x1b[33m"email"\x1b[39;49;00m
\x1b[34mFROM\x1b[39;49;00m \x1b[33m"auth_user"\x1b[39;49;00m
\x1b[34mWHERE\x1b[39;49;00m \x1b[33m"auth_user"\x1b[39;49;00m.\x1b[33m"id"\x1b[39;49;00m = \x1b[33m\'1\'\x1b[39;49;00m'''

snapshots['SnapshotQueriesTest::test_multiple_queries_duplicates 1'] = '''

============================
2 duplicate queries detected
============================
Query 1
---------
< 1 ms

/python/tests/test_django/tests/test_snapshot_queries.py:30 in test_multiple_queries_duplicates

\x1b[36mlist\x1b[39;49;00m(User.objects.only(\x1b[33m"\x1b[39;49;00m\x1b[33mid\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m).filter(\x1b[36mid\x1b[39;49;00m=\x1b[34m1\x1b[39;49;00m))

\x1b[34mSELECT\x1b[39;49;00m \x1b[33m"auth_user"\x1b[39;49;00m.\x1b[33m"id"\x1b[39;49;00m
\x1b[34mFROM\x1b[39;49;00m \x1b[33m"auth_user"\x1b[39;49;00m
\x1b[34mWHERE\x1b[39;49;00m \x1b[33m"auth_user"\x1b[39;49;00m.\x1b[33m"id"\x1b[39;49;00m = \x1b[33m\'1\'\x1b[39;49;00m


Query 2
---------
< 1 ms

/python/tests/test_django/tests/test_snapshot_queries.py:31 in test_multiple_queries_duplicates

\x1b[36mlist\x1b[39;49;00m(User.objects.only(\x1b[33m"\x1b[39;49;00m\x1b[33mid\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m).filter(\x1b[36mid\x1b[39;49;00m=\x1b[34m1\x1b[39;49;00m))

\x1b[34mSELECT\x1b[39;49;00m \x1b[33m"auth_user"\x1b[39;49;00m.\x1b[33m"id"\x1b[39;49;00m
\x1b[34mFROM\x1b[39;49;00m \x1b[33m"auth_user"\x1b[39;49;00m
\x1b[34mWHERE\x1b[39;49;00m \x1b[33m"auth_user"\x1b[39;49;00m.\x1b[33m"id"\x1b[39;49;00m = \x1b[33m\'1\'\x1b[39;49;00m'''

snapshots['SnapshotQueriesTest::test_multiple_queries_similar 1'] = '''

==========================
2 similar queries detected
==========================
Query 1
---------
< 1 ms

/python/tests/test_django/tests/test_snapshot_queries.py:41 in test_multiple_queries_similar

\x1b[36mlist\x1b[39;49;00m(User.objects.only(\x1b[33m"\x1b[39;49;00m\x1b[33memail\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m).filter(\x1b[36mid\x1b[39;49;00m=\x1b[34m1\x1b[39;49;00m))

\x1b[34mSELECT\x1b[39;49;00m \x1b[33m"auth_user"\x1b[39;49;00m.\x1b[33m"id"\x1b[39;49;00m,
       \x1b[33m"auth_user"\x1b[39;49;00m.\x1b[33m"email"\x1b[39;49;00m
\x1b[34mFROM\x1b[39;49;00m \x1b[33m"auth_user"\x1b[39;49;00m
\x1b[34mWHERE\x1b[39;49;00m \x1b[33m"auth_user"\x1b[39;49;00m.\x1b[33m"id"\x1b[39;49;00m = \x1b[33m\'1\'\x1b[39;49;00m


Query 2
---------
< 1 ms

/python/tests/test_django/tests/test_snapshot_queries.py:42 in test_multiple_queries_similar

\x1b[36mlist\x1b[39;49;00m(User.objects.only(\x1b[33m"\x1b[39;49;00m\x1b[33memail\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m).filter(\x1b[36mid\x1b[39;49;00m=\x1b[34m2\x1b[39;49;00m))

\x1b[34mSELECT\x1b[39;49;00m \x1b[33m"auth_user"\x1b[39;49;00m.\x1b[33m"id"\x1b[39;49;00m,
       \x1b[33m"auth_user"\x1b[39;49;00m.\x1b[33m"email"\x1b[39;49;00m
\x1b[34mFROM\x1b[39;49;00m \x1b[33m"auth_user"\x1b[39;49;00m
\x1b[34mWHERE\x1b[39;49;00m \x1b[33m"auth_user"\x1b[39;49;00m.\x1b[33m"id"\x1b[39;49;00m = \x1b[33m\'2\'\x1b[39;49;00m'''

snapshots['SnapshotQueriesTest::test_single_query_display_string 1'] = '''Query 1
---------
< 1 ms

/python/tests/test_django/tests/test_snapshot_queries.py:14 in test_single_query_display_string

\x1b[36mlist\x1b[39;49;00m(User.objects.only(\x1b[33m"\x1b[39;49;00m\x1b[33memail\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m).filter(\x1b[36mid\x1b[39;49;00m=\x1b[34m1\x1b[39;49;00m))

\x1b[34mSELECT\x1b[39;49;00m \x1b[33m"auth_user"\x1b[39;49;00m.\x1b[33m"id"\x1b[39;49;00m,
       \x1b[33m"auth_user"\x1b[39;49;00m.\x1b[33m"email"\x1b[39;49;00m
\x1b[34mFROM\x1b[39;49;00m \x1b[33m"auth_user"\x1b[39;49;00m
\x1b[34mWHERE\x1b[39;49;00m \x1b[33m"auth_user"\x1b[39;49;00m.\x1b[33m"id"\x1b[39;49;00m = \x1b[33m\'1\'\x1b[39;49;00m'''