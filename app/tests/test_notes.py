import os
import json
import pytest
from fastapi.testclient import TestClient
from starlette import status

from app.main import app
import app.storage as storage


def test_create_note():
    client = TestClient(app)
    request = client.post("/notes", json = {"title": "t1",
                                            "content": "c1"})

    assert request.status_code == status.HTTP_201_CREATED

    response = request.json()

    assert response["id"] == 1
    assert response["title"] == "t1"
    assert response["content"] == "c1"

def test_list_notes():
    client = TestClient(app)

    client.post("/notes", json = {"title": "t1","content":"c1"})

    request = client.get("/notes")
    assert request.status_code == status.HTTP_200_OK

    response = request.json()
    assert len(response) == 1
    assert response[0]["id"] == 1

def test_get_note():
    client = TestClient(app)

    request = client.get("/notes/1")
    assert request.status_code == status.HTTP_404_NOT_FOUND

def test_delete_note():
    client = TestClient(app)
    client.post("/notes", json = {"title": "t1","content":"c1"})
    length = client.get("/notes")
    request = client.delete("/notes/1")
    data = length.json()
    assert request.status_code == status.HTTP_204_NO_CONTENT
    assert len(data) == 0



