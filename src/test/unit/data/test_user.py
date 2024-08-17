import os
import pytest

from model.user import User
from data import user
from errors import Missing, Duplicate

from data.init import get_or_create_db


DB_PATH = get_or_create_db(DB_NAME='test')[1]

@pytest.fixture
def sample() -> User:
    return User(name="resident_evil", hash="resident_evil")

def test_create(sample: User):
    response = user.create(user=sample)
    assert response == sample

def test_create_duplicate(sample: User):
    with pytest.raises(Duplicate):
        user.create(user=sample)

def test_get_one(sample: User):
    response = user.get_one(name=sample.name)
    assert response == sample
    
def test_get_one_missing():
    with pytest.raises(Missing):
        user.get_one(name="silent_hill")

def test_modify(sample: User):
    sample.hash = 'silent_hill'
    response = user.modify(name=sample.name, user=sample)
    assert response == sample

def test_modify_missing():
    thing = User(name="metro_2033", hash="metro_2033")
    with pytest.raises(Missing):
        user.modify(name=thing.name, user=thing)

def test_delete(sample: User):
    response = user.delete(name=sample.name)
    assert response is True

def test_delete_missing(sample: User):
    with pytest.raises(Missing):
        user.delete(name=sample.name)

os.remove(path=DB_PATH)