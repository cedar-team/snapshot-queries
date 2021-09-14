# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestSQLite::test_executing_queries 1'] = '''Query 1
---------
/python/tests/test_sqlalchemy/test_sqlite.py:46 in test_executing_queries

id=1, first_name="Juan", last_name="Gonzalez"

INSERT INTO students (id, first_name, last_name)
VALUES (1, 'Juan', 'Gonzalez')


Query 2
---------
/python/tests/test_sqlalchemy/test_sqlite.py:52 in test_executing_queries

id=1, name="Computer Science 101", start_date=date(2020, 1, 1)

INSERT INTO classes (id, name, start_date)
VALUES (1, 'Computer Science 101', '2020-01-01')


Query 3
---------
/python/tests/test_sqlalchemy/test_sqlite.py:56 in test_executing_queries

conn.execute(self.students.select())

SELECT students.id,
       students.first_name,
       students.last_name
FROM students


Query 4
---------
/python/tests/test_sqlalchemy/test_sqlite.py:57 in test_executing_queries

conn.execute(self.classes.select())

SELECT classes.id,
       classes.name,
       classes.start_date
FROM classes'''
