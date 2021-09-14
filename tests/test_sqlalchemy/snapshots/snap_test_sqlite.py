# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['SnapshotTestCase::test_executing_queries 1'] = '''Query 1
---------
< 1 ms

/python/tests/test_sqlalchemy/test_sqlite.py:44 in test_executing_queries

conn.execute(

\x1b[34mINSERT\x1b[39;49;00m \x1b[34mINTO\x1b[39;49;00m students (id, first_name, last_name)
\x1b[34mVALUES\x1b[39;49;00m (\x1b[34m1\x1b[39;49;00m, \x1b[33m'Juan'\x1b[39;49;00m, \x1b[33m'Gonzalez'\x1b[39;49;00m)


Query 2
---------
< 1 ms

/python/tests/test_sqlalchemy/test_sqlite.py:50 in test_executing_queries

conn.execute(

\x1b[34mINSERT\x1b[39;49;00m \x1b[34mINTO\x1b[39;49;00m classes (id, name, start_date)
\x1b[34mVALUES\x1b[39;49;00m (\x1b[34m1\x1b[39;49;00m, \x1b[33m'Computer Science 101'\x1b[39;49;00m, \x1b[33m'2020-01-01'\x1b[39;49;00m)


Query 3
---------
< 1 ms

/python/tests/test_sqlalchemy/test_sqlite.py:56 in test_executing_queries

conn.execute(\x1b[36mself\x1b[39;49;00m.students.select())

\x1b[34mSELECT\x1b[39;49;00m students.id,
       students.first_name,
       students.last_name
\x1b[34mFROM\x1b[39;49;00m students


Query 4
---------
< 1 ms

/python/tests/test_sqlalchemy/test_sqlite.py:57 in test_executing_queries

conn.execute(\x1b[36mself\x1b[39;49;00m.classes.select())

\x1b[34mSELECT\x1b[39;49;00m classes.id,
       classes.name,
       classes.start_date
\x1b[34mFROM\x1b[39;49;00m classes'''

snapshots['TestSQLite::test_executing_queries 1'] = '''Query 1
---------
< 1 ms

/python/tests/test_sqlalchemy/test_sqlite.py:46 in test_executing_queries

\x1b[36mid\x1b[39;49;00m=\x1b[34m1\x1b[39;49;00m, first_name=\x1b[33m"\x1b[39;49;00m\x1b[33mJuan\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m, last_name=\x1b[33m"\x1b[39;49;00m\x1b[33mGonzalez\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m

\x1b[34mINSERT\x1b[39;49;00m \x1b[34mINTO\x1b[39;49;00m students (id, first_name, last_name)
\x1b[34mVALUES\x1b[39;49;00m (\x1b[34m1\x1b[39;49;00m, \x1b[33m'Juan'\x1b[39;49;00m, \x1b[33m'Gonzalez'\x1b[39;49;00m)


Query 2
---------
< 1 ms

/python/tests/test_sqlalchemy/test_sqlite.py:52 in test_executing_queries

\x1b[36mid\x1b[39;49;00m=\x1b[34m1\x1b[39;49;00m, name=\x1b[33m"\x1b[39;49;00m\x1b[33mComputer Science 101\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m, start_date=date(\x1b[34m2020\x1b[39;49;00m, \x1b[34m1\x1b[39;49;00m, \x1b[34m1\x1b[39;49;00m)

\x1b[34mINSERT\x1b[39;49;00m \x1b[34mINTO\x1b[39;49;00m classes (id, name, start_date)
\x1b[34mVALUES\x1b[39;49;00m (\x1b[34m1\x1b[39;49;00m, \x1b[33m'Computer Science 101'\x1b[39;49;00m, \x1b[33m'2020-01-01'\x1b[39;49;00m)


Query 3
---------
< 1 ms

/python/tests/test_sqlalchemy/test_sqlite.py:56 in test_executing_queries

conn.execute(\x1b[36mself\x1b[39;49;00m.students.select())

\x1b[34mSELECT\x1b[39;49;00m students.id,
       students.first_name,
       students.last_name
\x1b[34mFROM\x1b[39;49;00m students


Query 4
---------
< 1 ms

/python/tests/test_sqlalchemy/test_sqlite.py:57 in test_executing_queries

conn.execute(\x1b[36mself\x1b[39;49;00m.classes.select())

\x1b[34mSELECT\x1b[39;49;00m classes.id,
       classes.name,
       classes.start_date
\x1b[34mFROM\x1b[39;49;00m classes'''
