from datetime import date

from snapshottest import TestCase
from sqlalchemy import (Column, Date, Integer, MetaData, String, Table,
                        create_engine)

from snapshot_queries import snapshot_queries


class TestPostgres(TestCase):
    maxDiff = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.engine = create_engine(
            f"postgresql+psycopg2://postgres:postgres@postgres-db/postgres"
        )

        meta = MetaData()

        cls.tables = []

        cls.students = Table(
            "students",
            meta,
            Column("id", Integer, primary_key=True),
            Column("first_name", String),
            Column("last_name", String),
        )
        cls.tables.append(cls.students)

        cls.classes = Table(
            "classes",
            meta,
            Column("id", Integer, primary_key=True),
            Column("name", String),
            Column("start_date", Date),
        )
        cls.tables.append(cls.classes)

        meta.create_all(cls.engine)

    def setUp(self):
        # Truncate the tables
        with self.engine.connect() as conn:
            for table in self.tables:
                conn.execute(table.delete())

    def test_executing_queries(self):
        with snapshot_queries() as queries:
            with self.engine.connect() as conn:
                conn.execute(
                    self.students.insert().values(
                        id=1, first_name="Juan", last_name="Gonzalez"
                    )
                )

                conn.execute(
                    self.classes.insert().values(
                        id=1, name="Computer Science 101", start_date=date(2020, 1, 1)
                    )
                )

                conn.execute(self.students.select())
                conn.execute(self.classes.select())

        self.assertMatchSnapshot(queries.display_string(colored=False, duration=False))
