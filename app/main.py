from fastapi import FastAPI
from app.routes.api import router as api_router
from contextlib import asynccontextmanager
from app.storage import load_notes


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_notes()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(api_router)