import os

import pytest

from model.explorer import Explorer
from errors import Missing

os.environ['CRYPTID_UNIT_TEST'] = 'True'

from service import explorer as code


@pytest.fixture(scope='session')
def delete_db():
    from data.creature import db_manager

    yield db_manager

    os.remove(path=db_manager.DB_PATH)

@pytest.fixture
def sample(delete_db) -> Explorer:
    return Explorer(name='Metro 2033', country='RU', description='Metro 2033')

def test_create(delete_db, sample: Explorer):
    response = code.create(explorer=sample)
    assert response == sample

def test_get_exists(delete_db, sample: Explorer):
    response = code.get_one(name='Metro 2033')
    assert response == sample

def test_get_missing(delete_db):
    with pytest.raises(Missing):
        code.get_one(name='Resident Evil')