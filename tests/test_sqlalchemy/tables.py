from sqlalchemy import Column, Date, Integer, MetaData, String, Table

tables = MetaData()

students = Table(
    "students",
    tables,
    Column("id", Integer, primary_key=True),
    Column("first_name", String),
    Column("last_name", String),
)

classes = Table(
    "classes",
    tables,
    Column("id", Integer, primary_key=True),
    Column("name", String),
    Column("start_date", Date),
)
