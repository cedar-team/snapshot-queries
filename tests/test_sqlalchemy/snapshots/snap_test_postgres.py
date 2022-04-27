# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots[
    "TestPostgres::test_executing_queries 1"
] = """Query 1
---------
test_postgres.py:53 in test_executing_queries

conn.execute(

INSERT INTO students (id, first_name, last_name)
VALUES (1, Juan, Gonzalez)


Query 2
---------
test_postgres.py:59 in test_executing_queries

conn.execute(

INSERT INTO classes (id, name, start_date)
VALUES (1, Computer Science 101, 2020-01-01)


Query 3
---------
test_postgres.py:65 in test_executing_queries

conn.execute(self.students.select())

SELECT students.id,
       students.first_name,
       students.last_name
FROM students


Query 4
---------
test_postgres.py:66 in test_executing_queries

conn.execute(self.classes.select())

SELECT classes.id,
       classes.name,
       classes.start_date
FROM classes"""
