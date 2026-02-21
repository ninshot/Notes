import os
import pytest
from httpx import AsyncClient, ASGITransport


from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from app.main import app
from app.database.db import get_async_session, Base

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

engine = create_async_engine(TEST_DATABASE_URL, echo=False, poolclass=NullPool)
TestingSessionLocal = async_sessionmaker(bind=engine, class_ = AsyncSession, expire_on_commit=False)

"""
    This fixture prepares the test database before running tests
    It runs once per test session, creating all tables before tests and dropping them after tests
    pytest will run it automatically because of autouse=True
"""
@pytest.fixture(scope="session", autouse=True)
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()

"""
    This fixture provides a new asynchronous session for each test function
    It ensures that each test runs in isolation with a fresh database session
    Performs a rollback after each test to clean up any changes made during the test
"""
@pytest.fixture(scope="function")
async def async_session():
    async with TestingSessionLocal() as session:
        yield session
        await session.rollback()

"""
    This fixture provides an AsyncClient for testing FastAPI endpoints
    It overrides the get_async_session db dependency to use the test database session
    Ensures the FastAPI app uses the test database during tests
"""
@pytest.fixture(scope="function")
async def client():

    async def override_get_async_session():
        async with TestingSessionLocal() as async_session:
            yield async_session

    app.dependency_overrides[get_async_session] = override_get_async_session

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()