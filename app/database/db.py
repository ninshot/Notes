from collections.abc import AsyncGenerator
import uuid

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import Column, String, ForeignKey, DateTime, Boolean, func, Integer, Nullable
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone

DATABASE_URL = "postgresql+asyncpg://postgres:password@localhost:5432/mydb"

class Base(DeclarativeBase):
    pass

class Notes(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True, nullable=False,autoincrement=True,unique=True)
    title = Column(String)
    content = Column(String)
    created_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    #user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    #user = relationship("User", back_populates="notes")

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False,autoincrement=True,unique=True)
    full_name = Column(String,nullable=False)
    email = Column(String(255),nullable=False,unique=True)
    password = Column(String,nullable=False)
    disabled = Column(Boolean,nullable=False,default=False)
    created_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    #notes = relationship("Notes", back_populates="user")

engine = create_async_engine(DATABASE_URL)
async_session = async_sessionmaker(engine, expire_on_commit=False)

async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def close_db():
    await engine.dispose()

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
