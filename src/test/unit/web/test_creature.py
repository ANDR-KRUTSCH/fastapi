import os

import pytest

from fastapi import HTTPException

os.environ["CRYPTID_UNIT_TEST"] = "true"

from model.creature import Creature
from web import creature


@pytest.fixture
def sample() -> Creature:
    return Creature(name="dragon", description="Wings! Fire!", country="*", area="*", aka="firedrake")

@pytest.fixture
def fakes() -> list[Creature]:
    return creature.get_all()

def test_create(sample: Creature):
    response = creature.create(creature=sample)
    assert response == sample

def test_create_duplicate(fakes: list[Creature]):
    with pytest.raises(HTTPException) as exc:
        creature.create(creature=fakes[0])
        assert exc.value.status_code == 404
        assert "Duplicate" in exc.value.detail

def test_get_one(fakes: list[Creature]):
    response = creature.get_one(name=fakes[0].name)
    assert response == fakes[0]

def test_get_one_missing():
    with pytest.raises(HTTPException) as exc:
        creature.get_one(name="resident_evil")
        assert exc.value.status_code == 404
        assert "Missing" in exc.value.detail

def test_modify(fakes: list[Creature]):
    response = creature.modify(name=fakes[0].name, creature=fakes[0])
    assert response == fakes[0]

def test_modify_missing(sample: Creature):
    sample.name = 'resident_evil'
    with pytest.raises(HTTPException) as exc:
        creature.modify(name=sample.name, creature=sample)
        assert exc.value.status_code == 404
        assert "Missing" in exc.value.detail

def test_delete(fakes: list[Creature]):
    response = creature.delete(fakes[0].name)
    assert response is True

def test_delete_missing():
    with pytest.raises(HTTPException) as exc:
        creature.delete(name="silent_hill")
        assert exc.value.status_code == 404
        assert "Missing" in exc.value.detail