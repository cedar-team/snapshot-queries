# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots[
    "TestSQLite::test_executing_queries 1"
] = """Query 1
---------
/python/tests/test_sqlalchemy/transaction.py:10 in transaction

yield session

INSERT INTO classes (name, start_date)
VALUES ('CS 101', '2020-01-01')


Query 2
---------
/python/tests/test_sqlalchemy/test_sqlite.py:28 in test_executing_queries

session.execute(session.query(Students))

SELECT students.id AS students_id,
       students.first_name AS students_first_name,
       students.last_name AS students_last_name
FROM students


Query 3
---------
/python/tests/test_sqlalchemy/test_sqlite.py:29 in test_executing_queries

session.execute(session.query(Classes))

SELECT classes.id AS classes_id,
       classes.name AS classes_name,
       classes.start_date AS classes_start_date
FROM classes"""
