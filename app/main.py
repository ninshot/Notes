from fastapi import FastAPI
from app.routes.notes import router as notes_router
from app.routes.users import router as user_router
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.db import create_db



@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(notes_router)
app.include_router(user_router)