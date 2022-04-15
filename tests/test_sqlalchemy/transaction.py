from contextlib import contextmanager

import sqlalchemy.orm


@contextmanager
def transaction(engine):
    session = sqlalchemy.orm.Session(engine, autocommit=True)
    with session.begin():
        yield session
