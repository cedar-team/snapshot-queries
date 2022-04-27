# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots[
    "test_executing_queries 1"
] = """
4 Queries

INSERT INTO students (...)
VALUES (...)

INSERT INTO classes (...)
VALUES (...)

SELECT ...
FROM students

SELECT ...
FROM classes
"""
