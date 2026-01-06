from fastapi import FastAPI
from app.routes.notes import router as api_router
from app.routes.users import router as user_router
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(api_router)
app.include_router(user_router)