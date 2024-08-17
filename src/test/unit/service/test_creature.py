import os

import pytest

from model.creature import Creature
from service import creature as code
from errors import Missing

from data.init import get_or_create_db


DB_PATH = get_or_create_db(DB_NAME='test')[1]

sample = Creature(name='Yeti', country='CN', area='Himalayas', description='Hirsute Himalayan', aka='Abominable Snowman')

def test_create():
    response = code.create(creature=sample)
    assert response == sample

def test_get_exists():
    response = code.get_one(name='Yeti')
    assert response == sample

def test_get_missing():
    with pytest.raises(Missing):
        code.get_one(name='Boxturtle')

os.remove(path=DB_PATH)