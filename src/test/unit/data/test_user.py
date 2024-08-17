import os

import pytest

from model.user import User
from errors import Missing, Duplicate

os.environ['CRYPTID_UNIT_TEST'] = 'True'

from data import user


@pytest.fixture(scope='session')
def delete_db():
    from data.user import db_manager

    yield db_manager

    os.remove(path=db_manager.DB_PATH)

@pytest.fixture
def sample() -> User:
    return User(name="resident_evil", hash="resident_evil")

def test_create(delete_db, sample: User):
    response = user.create(user=sample)
    assert response == sample

def test_create_duplicate(delete_db, sample: User):
    with pytest.raises(Duplicate):
        user.create(user=sample)

def test_get_one(delete_db, sample: User):
    response = user.get_one(name=sample.name)
    assert response == sample
    
def test_get_one_missing(delete_db):
    with pytest.raises(Missing):
        user.get_one(name="silent_hill")

def test_modify(delete_db, sample: User):
    sample.hash = 'silent_hill'
    response = user.modify(name=sample.name, user=sample)
    assert response == sample

def test_modify_missing(delete_db):
    thing = User(name="metro_2033", hash="metro_2033")
    with pytest.raises(Missing):
        user.modify(name=thing.name, user=thing)

def test_delete(delete_db, sample: User):
    response = user.delete(name=sample.name)
    assert response is True

def test_delete_missing(delete_db, sample: User):
    with pytest.raises(Missing):
        user.delete(name=sample.name)