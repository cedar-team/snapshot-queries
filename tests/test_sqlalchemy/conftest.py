import pytest

from .tables import tables


@pytest.fixture
def setup_tables(db):
    tables.drop_all(db)
    tables.create_all(db)
