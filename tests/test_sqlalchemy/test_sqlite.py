from snapshottest import TestCase
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, Date
from snapshot_queries import snapshot_queries
from pathlib import Path
from datetime import date


class SnapshotTestCase(TestCase):
    maxDiff = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        db_file = Path("/tmp/college.db")
        if db_file.exists():
            db_file.unlink()

        cls.engine = create_engine(f"sqlite:///{db_file}")

        meta = MetaData()

        cls.students = Table(
            "students",
            meta,
            Column("id", Integer, primary_key=True),
            Column("first_name", String),
            Column("last_name", String),
        )

        cls.classes = Table(
            "classes",
            meta,
            Column("id", Integer, primary_key=True),
            Column("name", String),
            Column("start_date", Date),
        )

        meta.create_all(cls.engine)

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

        self.assertMatchSnapshot(queries.display_string())
