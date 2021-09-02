# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestPostgres::test_executing_queries 1'] = '''Query 1
---------
< 1 ms

/python/tests/test_sqlalchemy/test_postgres.py:57 in test_executing_queries

conn.execute(

\x1b[34mINSERT\x1b[39;49;00m \x1b[34mINTO\x1b[39;49;00m students (id, first_name, last_name)
\x1b[34mVALUES\x1b[39;49;00m (\x1b[34m1\x1b[39;49;00m, Juan, Gonzalez)


Query 2
---------
< 1 ms

/python/tests/test_sqlalchemy/test_postgres.py:63 in test_executing_queries

conn.execute(

\x1b[34mINSERT\x1b[39;49;00m \x1b[34mINTO\x1b[39;49;00m classes (id, \x1b[34mname\x1b[39;49;00m, start_date)
\x1b[34mVALUES\x1b[39;49;00m (\x1b[34m1\x1b[39;49;00m, Computer Science \x1b[34m101\x1b[39;49;00m, \x1b[34m2020\x1b[39;49;00m-\x1b[34m01\x1b[39;49;00m-\x1b[34m01\x1b[39;49;00m)


Query 3
---------
< 1 ms

/python/tests/test_sqlalchemy/test_postgres.py:69 in test_executing_queries

conn.execute(\x1b[36mself\x1b[39;49;00m.students.select())

\x1b[34mSELECT\x1b[39;49;00m students\x1b[34m.\x1b[39;49;00mid,
       students\x1b[34m.\x1b[39;49;00mfirst_name,
       students\x1b[34m.\x1b[39;49;00mlast_name
\x1b[34mFROM\x1b[39;49;00m students


Query 4
---------
< 1 ms

/python/tests/test_sqlalchemy/test_postgres.py:70 in test_executing_queries

conn.execute(\x1b[36mself\x1b[39;49;00m.classes.select())

\x1b[34mSELECT\x1b[39;49;00m classes\x1b[34m.\x1b[39;49;00mid,
       classes\x1b[34m.\x1b[39;49;00m\x1b[34mname\x1b[39;49;00m,
       classes\x1b[34m.\x1b[39;49;00mstart_date
\x1b[34mFROM\x1b[39;49;00m classes'''
