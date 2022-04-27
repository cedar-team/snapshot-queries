from datetime import date

import pytest
from sqlalchemy import create_engine

from .tables import classes, students


@pytest.fixture
def db():
    return create_engine("postgresql+psycopg2://postgres:postgres@postgres-db/postgres")


def test_executing_queries(queries_snapshot, db, setup_tables):
    with queries_snapshot.assert_match():
        with db.connect() as conn:
            conn.execute(
                students.insert().values(id=1, first_name="Juan", last_name="Gonzalez")
            )

            conn.execute(
                classes.insert().values(
                    id=1, name="Computer Science 101", start_date=date(2020, 1, 1)
                )
            )

            conn.execute(students.select())
            conn.execute(classes.select())
