import pytest
from starlette import status

"""Tests for user registration and login functionality."""

#Test Case 1: User Registration with valid data
@pytest.mark.asyncio
async def test_register_user(client):
    
    response = await client.post("/auth/register", data={
        "email": "test@example.com",
        "password": "1234",
        "fullname": "Test User"
        })
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["full_name"] == "Test User"
    assert data["id"] is not None

#Test Case 2: User Login with correct credentials
@pytest.mark.asyncio
async def test_register_with_duplicate_email(client):
    # First, register a user
    await client.post("/auth/register", data={
        "email": "test@example.com",
        "password": "1234",
        "fullname": "Test User"
        })

    # Second, attempt to register with the same email
    response = await client.post("/auth/register", data={
        "email": "test@example.com",
        "password": "1234",
        "fullname": "Test User"
        })
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST

#Test Case 3: User Login with correct credentials
@pytest.mark.asyncio
async def test_login_user(client):
    # First, register a user
    await client.post("/auth/register", data={
        "email": "test@example.com",
        "password": "1234",
        "fullname": "Test User"
        })

    # Then, login with the registered user's credentials
    response = await client.post("/auth/login", data={
        "username": "test@example.com",
        "password": "1234"
        })
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["token_type"] == "bearer"

#Test Case 4: User Login with incorrect credentials
@pytest.mark.asyncio
async def test_login_user_incorrect_credentials(client):
    # First, register a user
    await client.post("/auth/register", data={
        "email": "test@example.com",
        "password": "1234",
        "fullname": "Test User"
        })

    # Then, attempt to login with incorrect password
    response = await client.post("/auth/login", data={
        "username": "james@email.com",
        "password": "wrongpassword"
    })
    assert response.status_code == status.HTTP_400_BAD_REQUEST





