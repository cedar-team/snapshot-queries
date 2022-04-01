# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots[
    "test_executing_queries 1"
] = """Query 1
---------
/python/tests/test_sqlalchemy/test_sqlite.py:35 in test_executing_queries

session.execute(sqlalchemy.select(Students))

INSERT INTO classes (id, name, start_date)
VALUES (1, 'Computer Science 101', '2020-01-01')


Query 2
---------
/python/tests/test_sqlalchemy/test_sqlite.py:35 in test_executing_queries

session.execute(sqlalchemy.select(Students))

INSERT INTO students (id, first_name, last_name)
VALUES (1, 'Juan', 'Gonzalez')


Query 3
---------
/python/tests/test_sqlalchemy/test_sqlite.py:35 in test_executing_queries

session.execute(sqlalchemy.select(Students))

SELECT students.id,
       students.first_name,
       students.last_name
FROM students


Query 4
---------
/python/tests/test_sqlalchemy/test_sqlite.py:36 in test_executing_queries

session.execute(sqlalchemy.select(Classes))

SELECT classes.id,
       classes.name,
       classes.start_date
FROM classes"""

snapshots[
    "test_assert_queries_match_snapshot 1"
] = """
4 Queries

INSERT INTO classes (...)
VALUES (...)

INSERT INTO students (...)
VALUES (...)

SELECT ...
FROM students

SELECT ...
FROM classes
"""
