import pytest
from httpx import Response

from fastapi.testclient import TestClient

from model.creature import Creature
from main import app


client = TestClient(app)

@pytest.fixture()
def sample() -> Creature:
    return Creature(name="Resident Evil", country="US", area="Raccoon City", description="Resident Evil", aka="RE")

def test_create(sample: Creature):
    response: Response = client.post("/creature", json=dict(sample))
    assert response.status_code == 201

def test_create_duplicate(sample: Creature):
    response: Response = client.post("/creature", json=dict(sample))
    assert response.status_code == 404

def test_get_one(sample: Creature):
    response: Response = client.get(f"/creature/{sample.name}")
    assert response.json() == dict(sample)

def test_get_one_missing():
    response: Response = client.get("/creature/outlast")
    assert response.status_code == 404

def test_modify(sample: Creature):
    response: Response = client.patch(f"/creature/{sample.name}", json=dict(sample))
    assert response.json() == dict(sample)

def test_modify_missing(sample: Creature):
    response: Response = client.patch("/creature/outlast", json=dict(sample))
    assert response.status_code == 404

def test_delete(sample: Creature):
    response: Response = client.delete(f"/creature/{sample.name}")
    assert response.status_code == 200
    assert response.json() is True

def test_delete_missing(sample: Creature):
    response: Response = client.delete(f"/creature/{sample.name}")
    assert response.status_code == 404