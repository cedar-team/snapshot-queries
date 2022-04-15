# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots[
    "TestPostgres::test_executing_queries 1"
] = """Query 1
---------
/python/tests/test_sqlalchemy/transaction.py:10 in transaction

yield session

INSERT INTO students (first_name, last_name)
VALUES (Bobby, Tables) RETURNING students.id


Query 2
---------
/python/tests/test_sqlalchemy/test_postgres.py:30 in test_executing_queries

session.execute(session.query(Students))

SELECT students.id AS students_id,
       students.first_name AS students_first_name,
       students.last_name AS students_last_name
FROM students


Query 3
---------
/python/tests/test_sqlalchemy/test_postgres.py:31 in test_executing_queries

session.execute(session.query(Classes))

SELECT classes.id AS classes_id,
       classes.name AS classes_name,
       classes.start_date AS classes_start_date
FROM classes"""
