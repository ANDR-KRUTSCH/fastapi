import os

import pytest

from model.explorer import Explorer
from service import explorer as code
from errors import Missing

from data.init import get_or_create_db


DB_PATH = get_or_create_db(DB_NAME='test')[1]

sample = Explorer(name='Claude Hande', country='FR', description='Scarce during full moons')

def test_create():
    response = code.create(explorer=sample)
    assert response == sample

def test_get_exists():
    response = code.get_one(name='Claude Hande')
    assert response == sample

def test_get_missing():
    with pytest.raises(Missing):
        code.get_one(name='Andrew Krutsch')

os.remove(path=DB_PATH)