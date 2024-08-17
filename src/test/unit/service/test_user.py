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
def fakes() -> list[User]:
    return user.get_all()

def test_create(sample: User):
    response = user.create(user=sample)
    assert response == sample

def test_create_duplicate(fakes: list[User]):
    with pytest.raises(HTTPException) as exc:
        user.create(user=fakes[0])
        assert exc.value.status_code == 404

def test_get_one(fakes: list[User]):
    assert user.get_one(name=fakes[0].name) == fakes[0]

def test_get_one_missing():
    with pytest.raises(HTTPException) as exc:
        user.get_one(name='Outlast')
        assert exc.value.status_code == 404