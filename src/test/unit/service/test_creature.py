from model.creature import Creature
from service import creature as code


sample = Creature(name='Yeti', country='CN', area='Himalayas', description='Hirsute Himalayan', aka='Abominable Snowman')

def test_create():
    response = code.create(creature=sample)
    assert response == sample

def test_get_exists():
    response = code.get_one(name='Yeti')
    assert response == sample

def test_get_missing():
    response = code.get_one(name='Boxturtle')
    assert response is None