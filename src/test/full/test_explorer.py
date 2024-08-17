import pytest
from httpx import Response

from fastapi.testclient import TestClient

from model.explorer import Explorer
from main import app


client = TestClient(app)

@pytest.fixture()
def sample() -> Explorer:
    return Explorer(name="Resident Evil", country="US", area="Raccoon City", description="Resident Evil", aka="RE")

def test_create(sample: Explorer):
    response: Response = client.post("/explorer", json=dict(sample))
    assert response.status_code == 201

def test_create_duplicate(sample: Explorer):
    response: Response = client.post("/explorer", json=dict(sample))
    assert response.status_code == 404

def test_get_one(sample: Explorer):
    response: Response = client.get(f"/explorer/{sample.name}")
    assert response.json() == dict(sample)

def test_get_one_missing():
    response: Response = client.get("/explorer/outlast")
    assert response.status_code == 404

def test_modify(sample: Explorer):
    response: Response = client.patch(f"/explorer/{sample.name}", json=dict(sample))
    assert response.json() == dict(sample)

def test_modify_missing(sample: Explorer):
    response: Response = client.patch("/explorer/outlast", json=dict(sample))
    assert response.status_code == 404

def test_delete(sample: Explorer):
    response: Response = client.delete(f"/explorer/{sample.name}")
    assert response.status_code == 200
    assert response.json() is True

def test_delete_missing(sample: Explorer):
    response: Response = client.delete(f"/explorer/{sample.name}")
    assert response.status_code == 404