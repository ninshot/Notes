import pytest
from starlette import status

"""Tests for note creation and retrieval functionality."""

@pytest.mark.asyncio
async def test_create_note_with_auth(client, auth_token):
    data = {
        "title": "Test Note",
        "content": "This is a test note."}
    
    response = await client.post("/notes", json=data, headers = auth_token)

    assert response.status_code == status.HTTP_201_CREATED

@pytest.mark.asyncio
async def test_postnote_without_auth(client):
    data = {
        "title": "Test Note",
        "content": "This is a test note."}
    
    response = await client.post("/notes",json=data, headers = None)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.asyncio
async def test_get_all_notes_with_auth(client, auth_token):
    data = {
        "title": "Test Note",
        "content": "This is a test note."}
    
    response = await client.post("/notes", json=data, headers = auth_token)
    assert response.status_code == status.HTTP_201_CREATED

    response = await client.get("/notes", headers = auth_token)
    assert response.status_code == status.HTTP_200_OK
    notes = response.json()
    assert len(notes) >= 1

@pytest.mark.asyncio
async def test_get_all_notes_without_auth(client):
    response = await client.get("/notes", headers = None)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.asyncio
async def test_get_note_by_id_with_auth(client, auth_token):
    data = {
        "title": "Test Note",
        "content": "This is a test note."}
    
    response = await client.post("/notes", json=data, headers = auth_token)
    assert response.status_code == status.HTTP_201_CREATED
    note_id = response.json()["id"]

    response = await client.get(f"/notes/{note_id}", headers = auth_token)
    assert response.status_code == status.HTTP_200_OK
    note = response.json()
    assert note["title"] == "Test Note"
    assert note["content"] == "This is a test note."

@pytest.mark.asyncio
async def test_patch_note_by_id_with_auth(client, auth_token):
    data = {
        "title": "Test Note",
        "content": "This is a test note."}
    
    response = await client.post("/notes", json=data, headers = auth_token)
    assert response.status_code == status.HTTP_201_CREATED
    note_id = response.json()["id"]

    updated_data = {
        "title": "Updated Test Note",
        "content": "This is an updated test note."}

    response = await client.patch(f"/notes/{note_id}", json=updated_data, headers = auth_token)
    assert response.status_code == status.HTTP_200_OK
    note = response.json()
    assert note["title"] == "Updated Test Note"
    assert note["content"] == "This is an updated test note."

@pytest.mark.asyncio
async def test_delete_note_by_id_with_auth(client, auth_token):
    data = {
        "title": "Test Note",
        "content": "This is a test note."}
    
    response = await client.post("/notes", json=data, headers = auth_token)
    assert response.status_code == status.HTTP_201_CREATED
    note_id = response.json()["id"]

    response = await client.delete(f"/notes/{note_id}", headers = auth_token)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = await client.get(f"/notes/{note_id}", headers = auth_token)
    assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.asyncio
async def test_delete_note_by_id_without_auth(client):
    data = {
        "title": "Test Note",
        "content": "This is a test note."}
    
    response = await client.post("/notes", json=data, headers = None)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED









    