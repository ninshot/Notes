from collections.abc import AsyncGenerator
import uuid

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import Column, String, ForeignKey, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone

DATABASE_URL = "postgresql+asyncpg://postgres:password@localhost:5432/mydb"

class Base(DeclarativeBase):
    pass

class Notes(Base):
    __tablename__ = "notes"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String)
    content = Column(String)
    created_at = Column(DateTime, default = datetime.now(timezone.utc))
    #user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    #user = relationship("User", back_populates="notes")

class Users(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    full_name = Column(String,nullable=False)
    email = Column(String,nullable=False)
    password = Column(String,nullable=False)
    disabled = Column(Boolean,nullable=False,default=False)
    created_at = Column(DateTime,nullable=False,default=datetime.now(timezone.utc))
    #notes = relationship("Notes", back_populates="user")

engine = create_async_engine(DATABASE_URL)
async_session = async_sessionmaker(engine, expire_on_commit=False)

async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def close_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_sessionmaker() as session:
        yield session
