
from fastapi import FastAPI
from app.routes.notes import router as notes_router
from app.routes.users import router as user_router
from contextlib import asynccontextmanager
from app.database.db import create_db, close_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db()
    yield
    await close_db()

app = FastAPI(lifespan=lifespan)
app.include_router(notes_router)
app.include_router(user_router)