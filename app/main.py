from fastapi import FastAPI
from app.routes.notes import router as api_router
from app.routes.users import router as user_router
from contextlib import asynccontextmanager
from app.storage import load_notes, load_users


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_notes()
    load_users()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(api_router)
app.include_router(user_router)