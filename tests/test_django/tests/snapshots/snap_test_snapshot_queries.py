# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots[
    "SnapshotQueriesTest::test_multiple_queries_display_string 1"
] = """Query 1
---------
/python/tests/test_django/tests/test_snapshot_queries.py:23 in test_multiple_queries_display_string

list(User.objects.only("id").filter(id=2))

SELECT "auth_user"."id"
FROM "auth_user"
WHERE "auth_user"."id" = \'2\'


Query 2
---------
/python/tests/test_django/tests/test_snapshot_queries.py:24 in test_multiple_queries_display_string

list(User.objects.only("email").filter(id=1))

SELECT "auth_user"."id",
       "auth_user"."email"
FROM "auth_user"
WHERE "auth_user"."id" = \'1\'"""

snapshots[
    "SnapshotQueriesTest::test_single_query_display_string 1"
] = """Query 1
---------
/python/tests/test_django/tests/test_snapshot_queries.py:16 in test_single_query_display_string

list(User.objects.only("email").filter(id=1))

SELECT "auth_user"."id",
       "auth_user"."email"
FROM "auth_user"
WHERE "auth_user"."id" = \'1\'"""

snapshots[
    "SnapshotQueriesTest::test_multiple_queries_duplicates 1"
] = """

============================
2 duplicate queries detected
============================
Query 1
---------
/python/tests/test_django/tests/test_snapshot_queries.py:32 in test_multiple_queries_duplicates

list(User.objects.only("id").filter(id=1))

SELECT "auth_user"."id"
FROM "auth_user"
WHERE "auth_user"."id" = \'1\'


Query 2
---------
/python/tests/test_django/tests/test_snapshot_queries.py:33 in test_multiple_queries_duplicates

list(User.objects.only("id").filter(id=1))

SELECT "auth_user"."id"
FROM "auth_user"
WHERE "auth_user"."id" = \'1\'"""

snapshots[
    "SnapshotQueriesTest::test_multiple_queries_similar 1"
] = """

==========================
2 similar queries detected
==========================
Query 1
---------
/python/tests/test_django/tests/test_snapshot_queries.py:45 in test_multiple_queries_similar

list(User.objects.only("email").filter(id=1))

SELECT "auth_user"."id",
       "auth_user"."email"
FROM "auth_user"
WHERE "auth_user"."id" = \'1\'


Query 2
---------
/python/tests/test_django/tests/test_snapshot_queries.py:46 in test_multiple_queries_similar

list(User.objects.only("email").filter(id=2))

SELECT "auth_user"."id",
       "auth_user"."email"
FROM "auth_user"
WHERE "auth_user"."id" = \'2\'"""

snapshots[
    "SnapshotQueriesTest::test_assert_queries_match 1"
] = """
3 Queries

SELECT ...
FROM "auth_user"
WHERE "auth_user"."id" = %s

SELECT ...
FROM "auth_user"
WHERE "auth_user"."id" = %s

SELECT ...
FROM "auth_user"
WHERE "auth_user"."id" = %s
"""
