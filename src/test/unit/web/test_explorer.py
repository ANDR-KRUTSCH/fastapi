import os

import pytest

from fastapi import HTTPException

os.environ["CRYPTID_UNIT_TEST"] = "true"

from model.explorer import Explorer
from web import explorer


@pytest.fixture
def sample() -> Explorer:
    return Explorer(name="Pa Tuohy", description="Gaelic gaffer", country="IE")

@pytest.fixture
def fakes() -> list[Explorer]:
    return explorer.get_all()

def test_create(sample: Explorer):
    response = explorer.create(explorer=sample)
    assert response == sample

def test_create_duplicate(fakes: list[Explorer]):
    with pytest.raises(HTTPException) as exc:
        explorer.create(explorer=fakes[0])
        assert exc.value.status_code == 404
        assert "Duplicate" in exc.value.detail

def test_get_one(fakes: list[Explorer]):
    response = explorer.get_one(name=fakes[0].name)
    assert response == fakes[0]

def test_get_one_missing():
    with pytest.raises(HTTPException) as exc:
        explorer.get_one("Buffy")
        assert exc.value.status_code == 404
        assert "Missing" in exc.value.detail

def test_modify(fakes: list[Explorer]):
    response = explorer.modify(name=fakes[0].name, explorer=fakes[0])
    assert response == fakes[0]

def test_modify_missing(sample: Explorer):
    sample.name = 'resident_evil'
    with pytest.raises(HTTPException) as exc:
        explorer.modify(name=sample.name, explorer=sample)
        assert exc.value.status_code == 404
        assert "Missing" in exc.value.detail

def test_delete(fakes: list[Explorer]):
    response = explorer.delete(name=fakes[0].name)
    assert response is True

def test_delete_missing():
    with pytest.raises(HTTPException) as exc:
        explorer.delete(name="Wally")
        assert exc.value.status_code == 404
        assert "Missing" in exc.value.detail