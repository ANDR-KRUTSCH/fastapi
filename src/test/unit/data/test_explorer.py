import os

import pytest

from model.explorer import Explorer
from errors import Missing, Duplicate

os.environ['CRYPTID_UNIT_TEST'] = 'True'

from data import explorer


@pytest.fixture(scope='session')
def delete_db():
    from data.explorer import db_manager

    yield db_manager

    os.remove(path=db_manager.DB_PATH)

@pytest.fixture
def sample() -> Explorer:
    return Explorer(name="Andrew", country="TJ", description="Programmer")

def test_create(delete_db, sample: Explorer):
    response = explorer.create(explorer=sample)
    assert response == sample

def test_create_duplicate(delete_db, sample: Explorer):
    with pytest.raises(Duplicate):
        explorer.create(explorer=sample)

def test_get_one(delete_db, sample: Explorer):
    response = explorer.get_one(name=sample.name)
    assert response == sample

def test_get_one_missing(delete_db):
    with pytest.raises(Missing):
        explorer.get_one(name='Maria')
    
def test_modify(delete_db, sample: Explorer):
    sample.country = 'DE'
    response = explorer.modify(name=sample.name, explorer=sample)
    assert response == sample

def test_modify_missing(delete_db):
    thing = Explorer(name="Leon", country="US", description="Policer")
    with pytest.raises(Missing):
        explorer.modify(name=thing.name, explorer=thing)

def test_delete(delete_db, sample: Explorer):
    response = explorer.delete(name=sample.name)
    assert response is True

def test_delete_missing(delete_db, sample: Explorer):
    with pytest.raises(Missing):
        explorer.delete(name=sample.name)