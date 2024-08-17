import os

import pytest

from fastapi import HTTPException

from model.user import User

os.environ['CRYPTID_UNIT_TEST'] = 'True'

from web import user


@pytest.fixture
def sample() -> User:
    return User(name='Metro 2033', hash='Metro 2033')

@pytest.fixture
def fakes() -> list[User] | list:
    return user.get_all()

def test_create(sample: User):
    response = user.create(user=sample)
    assert response == sample

def test_create_duplicate(fakes: list):
    with pytest.raises(HTTPException) as exc:
        user.create(user=fakes[0])
        assert exc.value.status_code == 404
        assert 'Duplicate' in exc.value.detail

def test_get_one(fakes: list):
    assert user.get_one(name=fakes[0].name) == fakes[0]

def test_get_one_missing():
    with pytest.raises(HTTPException) as exc:
        user.get_one(name='Metro 2033')
        assert exc.value.status_code == 404
        assert 'Missing' in exc.value.detail

def test_modify(fakes: list):
    assert user.modify(name=fakes[0].name, user=fakes[0]) == fakes[0]

def test_modify_missing(sample: User):
    with pytest.raises(HTTPException) as exc:
        user.modify(name=sample.name, user=sample)
        assert exc.value.status_code == 404
        assert 'Missing' in exc.value.detail

def test_delete(fakes: list):
    assert user.delete(name=fakes[0].name) is True

def test_delete_missing():
    with pytest.raises(HTTPException) as exc:
        user.delete('Metro 2033')
        assert exc.value.status_code == 404
        assert 'Missing' in exc.value.detail