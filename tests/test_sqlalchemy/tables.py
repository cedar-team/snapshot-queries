from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy

Tables = declarative_base()


class Students(Tables):
    __tablename__ = "students"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    first_name = sqlalchemy.Column(sqlalchemy.String)
    last_name = sqlalchemy.Column(sqlalchemy.String)


class Classes(Tables):
    __tablename__ = "classes"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    start_date = sqlalchemy.Column(sqlalchemy.Date)

