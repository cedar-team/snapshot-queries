from snapshottest import TestCase
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, Date
from snapshot_queries import snapshot_queries
from pathlib import Path
from datetime import date


class TestPostgres(TestCase):
    maxDiff = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.engine = create_engine(f"postgresql+psycopg2://postgres:postgres@postgres-db/postgres")

        meta = MetaData()

        conn = cls.engine.connect()
        trans = conn.begin()
        for table in meta.sorted_tables:
            conn.execute(table.delete())
        trans.commit()

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

        import ipdb; ipdb.set_trace()
        self.assertMatchSnapshot(queries.display_string())
