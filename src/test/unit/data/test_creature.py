import os
import pytest

from model.creature import Creature
from errors import Missing, Duplicate

os.environ['CRYPTID_SQLITE_DB'] = 'test'

from data import creature


@pytest.fixture
def sample() -> Creature:
    return Creature(name="Yeti", country="CN", area="Himalayas", description="Harmless Himalayan", aka="Abominable Snowman")

def test_create(sample: Creature):
    response = creature.create(creature=sample)
    assert response == sample

def test_create_duplicate(sample: Creature):
    with pytest.raises(Duplicate):
        creature.create(sample)

def test_get_one(sample: Creature):
    response = creature.get_one(name=sample.name)
    assert response == sample

def test_get_one_missing():
    with pytest.raises(Missing):
        creature.get_one(name='Boxturtle')
    
def test_modify(sample: Creature):
    sample.area = 'Sesame Street'
    response = creature.modify(name=sample.name, creature=sample)
    assert response == sample

def test_modify_missing():
    thing = Creature(name='Snurfle', country='RU', area='', description='some thing', aka='')
    with pytest.raises(Missing):
        creature.modify(name=thing.name, creature=thing)

def test_delete(sample: Creature):
    response = creature.delete(name=sample.name)
    assert response is True

def test_delete_missing(sample: Creature):
    with pytest.raises(Missing):
        creature.delete(name=sample.name)