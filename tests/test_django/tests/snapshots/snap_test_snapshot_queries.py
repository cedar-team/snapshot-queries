# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots[
    "SnapshotQueriesTest::test_multiple_queries_display_string 1"
] = """
2 Queries

SELECT ...
FROM "auth_user"
WHERE "auth_user"."id" = %s

SELECT ...
FROM "auth_user"
WHERE "auth_user"."id" = %s
"""

snapshots[
    "SnapshotQueriesTest::test_single_query_display_string 1"
] = """
1 Queries

SELECT ...
FROM "auth_user"
WHERE "auth_user"."id" = %s
"""

snapshots[
    "SnapshotQueriesTest::test_multiple_queries_duplicates 1"
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

snapshots[
    "SnapshotQueriesTest::test_multiple_queries_similar 1"
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
