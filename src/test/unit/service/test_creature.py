import os

import pytest

from model.creature import Creature
from errors import Missing

os.environ['CRYPTID_UNIT_TEST'] = 'True'

from service import creature as code


@pytest.fixture(scope='session')
def delete_db():
    from data.creature import db_manager

    yield db_manager

    os.remove(path=db_manager.DB_PATH)

@pytest.fixture
def sample(delete_db) -> Creature:
    return Creature(name='Metro 2033', country='RU', area='Moscow', description='Metro 2033', aka='Metro 2033') 

def test_create(delete_db, sample: Creature):
    response = code.create(creature=sample)
    assert response == sample

def test_get_exists(delete_db, sample: Creature):
    response = code.get_one(name='Metro 2033')
    assert response == sample

def test_get_missing(delete_db):
    with pytest.raises(Missing):
        code.get_one(name='Resident Evil')