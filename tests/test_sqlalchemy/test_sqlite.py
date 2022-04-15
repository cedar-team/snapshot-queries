from datetime import date

from snapshottest import TestCase
from sqlalchemy import create_engine

from snapshot_queries import snapshot_queries

from .tables import Classes, Students, Tables
from .transaction import transaction


def engine():
    return create_engine(f"sqlite:////tmp/college.db")


class TestSQLite(TestCase):
    maxDiff = None

    def setUp(self):
        Tables.metadata.drop_all(engine())
        Tables.metadata.create_all(engine())

    def test_executing_queries(self):
        with snapshot_queries() as queries:
            with transaction(engine()) as session:
                session.execute(session.query(Students))
                session.execute(session.query(Classes))

        self.assertMatchSnapshot(queries.display_string(colored=False, duration=False))
