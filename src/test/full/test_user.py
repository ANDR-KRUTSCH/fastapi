import pytest
from httpx import Response

from fastapi.testclient import TestClient

from model.user import User
from main import app


client = TestClient(app)

@pytest.fixture
def sample() -> User:
    return User(name="Resident Evil", hash="Resident Evil")

def test_create(sample: User):
    response: Response = client.post("/user", json=dict(sample))
    assert response.status_code == 201

def test_create_duplicate(sample: User):
    response: Response = client.post("/user", json=dict(sample))
    assert response.status_code == 409

def test_get_one(sample: User):
    response: Response = client.get(f"/user/{sample.name}")
    user: dict = response.json() 
    assert user['name'] == sample.name

def test_get_one_missing():
    response: Response = client.get("/user/outlast")
    assert response.status_code == 404

def test_modify(sample: User):
    response: Response = client.patch(f"/user/{sample.name}", json=dict(sample))
    assert response.json() == dict(sample)

def test_modify_missing(sample: User):
    response: Response = client.patch("/user/outlast", json=dict(sample))
    assert response.status_code == 404

def test_delete(sample: User):
    response: Response = client.delete(f"/user/{sample.name}")
    assert response.json() is True
    assert response.status_code == 200

def test_delete_missing(sample: User):
    response: Response = client.delete(f"/user/{sample.name}")
    assert response.status_code == 404