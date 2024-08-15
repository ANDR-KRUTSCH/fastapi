from model.explorer import Explorer
from service import explorer as code

sample = Explorer(name='Claude Hande', country='FR', description='Scarce during full moons')

def test_create():
    response = code.create(explorer=sample)
    assert response == sample

def test_get_exists():
    response = code.get_one(name='Claude Hande')
    assert response == sample

def test_get_missing():
    response = code.get_one(name='Andrew Krutsch')
    assert response is None