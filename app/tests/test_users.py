import pytest
from fastapi.testclient import TestClient
from starlette import status

from app.main import app
import app.storage as storage

@pytest.fixture(autouse=True)
def client():
    return TestClient(app)


@pytest.fixture(autouse=True)
def temp_user_storage(tmp_path):

    storage.USERS_PATH = tmp_path / "users.json"

    storage.user_db.clear()
    storage.user_id = 1

    yield

    storage.user_db.clear()
    storage.user_id = 1


def test_create_user(client):

    request = client.post("/users", json={
        "email" : "test@email.com",
        "password" : "test@123",
        "full_name" : "test",
    })
    assert request.status_code == status.HTTP_201_CREATED

    response = request.json()

    assert response["email"] == "test@email.com"
    assert response["id"] == 1
    assert response["full_name"] == "test"

def test_get_user(client):
    request = client.post("/users", json={
        "email": "test@email.com",
        "password": "test@123",
        "full_name": "test",
    })

    request = client.get("/users/1")

    response = request.json()
    print(response)

    assert response["email"] == "test@email.com"
    assert response["id"] == 1
    assert response["full_name"] == "test"

def test_update_user(client):
    request = client.post("/users", json={
        "email": "test@email.com",
        "password": "test@123",
        "full_name": "test",
    })

    request = client.patch("/users/1", json={})

    assert request.status_code == status.HTTP_409_CONFLICT

    request = client.patch("/users/1", json={"email": "update21@email.com", "password": "","full_name": "jacks",})
    assert request.status_code == status.HTTP_200_OK
    response = request.json()
    assert response["email"] == "update21@email.com"

def test_delete_user(client):
    request = client.post("/users", json={
        "email": "test@email.com",
        "password": "test@123",
        "full_name": "test",
    })

    request = client.delete("/users/1")
    assert request.status_code == status.HTTP_204_NO_CONTENT

    request = client.delete("/users/1")
    assert request.status_code == status.HTTP_404_NOT_FOUND


