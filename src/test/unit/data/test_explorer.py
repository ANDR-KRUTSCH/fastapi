import os
import pytest

from model.explorer import Explorer
from data import explorer
from errors import Missing, Duplicate

from data.init import get_or_create_db


DB_PATH = get_or_create_db(DB_NAME='test')[1]

@pytest.fixture
def sample() -> Explorer:
    return Explorer(name="Andrew", country="TJ", description="Programmer")

def test_create(sample: Explorer):
    response = explorer.create(explorer=sample)
    assert response == sample

def test_create_duplicate(sample: Explorer):
    with pytest.raises(Duplicate):
        explorer.create(explorer=sample)

def test_get_one(sample: Explorer):
    response = explorer.get_one(name=sample.name)
    assert response == sample

def test_get_one_missing():
    with pytest.raises(Missing):
        explorer.get_one(name='Maria')
    
def test_modify(sample: Explorer):
    sample.country = 'DE'
    response = explorer.modify(name=sample.name, explorer=sample)
    assert response == sample

def test_modify_missing():
    thing = Explorer(name="Leon", country="US", description="Policer")
    with pytest.raises(Missing):
        explorer.modify(name=thing.name, explorer=thing)

def test_delete(sample: Explorer):
    response = explorer.delete(name=sample.name)
    assert response is True

def test_delete_missing(sample: Explorer):
    with pytest.raises(Missing):
        explorer.delete(name=sample.name)

os.remove(path=DB_PATH)