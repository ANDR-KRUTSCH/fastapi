import os

import pytest

from model.creature import Creature
from errors import Missing, Duplicate

os.environ['CRYPTID_UNIT_TEST'] = 'True'

from data import creature


@pytest.fixture(scope='session')
def delete_db():
    from data.creature import db_manager

    yield db_manager

    os.remove(path=db_manager.DB_PATH)

@pytest.fixture
def sample() -> Creature:
    return Creature(name="Yeti", country="CN", area="Himalayas", description="Harmless Himalayan", aka="Abominable Snowman")

def test_create(delete_db, sample: Creature):
    response = creature.create(creature=sample)
    assert response == sample

def test_create_duplicate(delete_db, sample: Creature):
    with pytest.raises(Duplicate):
        creature.create(sample)

def test_get_one(delete_db, sample: Creature):
    response = creature.get_one(name=sample.name)
    assert response == sample

def test_get_one_missing(delete_db):
    with pytest.raises(Missing):
        creature.get_one(name='Boxturtle')
    
def test_modify(delete_db, sample: Creature):
    sample.area = 'Sesame Street'
    response = creature.modify(name=sample.name, creature=sample)
    assert response == sample

def test_modify_missing(delete_db):
    thing = Creature(name='Snurfle', country='RU', area='', description='some thing', aka='')
    with pytest.raises(Missing):
        creature.modify(name=thing.name, creature=thing)

def test_delete(delete_db, sample: Creature):
    response = creature.delete(name=sample.name)
    assert response is True

def test_delete_missing(delete_db, sample: Creature):
    with pytest.raises(Missing):
        creature.delete(name=sample.name)