from snapshottest import TestCase
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, Date
from snapshot_queries import snapshot_queries
from snapshot_queries.testing import SnapshotQueriesTestCase
from pathlib import Path
from datetime import date
import pytest
from .tables import Students, Classes, Tables
import sqlalchemy.orm

db_file = Path("/tmp/college.db")

def get_engine():
    return create_engine(f"sqlite:///{db_file}")


@pytest.fixture
def db_tables():
    engine = get_engine()
    Tables.metadata.drop_all(engine)
    Tables.metadata.create_all(engine)


def test_executing_queries(snapshot, db_tables):
    with snapshot_queries() as queries:
        with sqlalchemy.orm.Session(get_engine(), future=True) as session:
            with session.begin():
                # INSERT a student and a class
                session.add(Students(id=1, first_name="Juan", last_name="Gonzalez"))
                session.add(
                    Classes(id=1, name="Computer Science 101", start_date=date(2020, 1, 1))
                )

                # SELECT all of the students and classes
                session.execute(sqlalchemy.select(Students))
                session.execute(sqlalchemy.select(Classes))

    snapshot.assert_match(queries.display_string(colored=False, duration=False))

def test_assert_queries_match_snapshot(snapshot_queries_fixture, db_tables):
    with snapshot_queries_fixture.assert_queries_match():
        with sqlalchemy.orm.Session(get_engine(), future=True) as session:
            with session.begin():
                # INSERT a student and a class
                session.add(Students(id=1, first_name="Juan", last_name="Gonzalez"))
                session.add(
                    Classes(id=1, name="Computer Science 101", start_date=date(2020, 1, 1))
                )

                # SELECT all of the students and classes
                session.execute(sqlalchemy.select(Students))
                session.execute(sqlalchemy.select(Classes))
