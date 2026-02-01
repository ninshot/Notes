from fastapi import APIRouter,HTTPException, status
from fastapi.params import Depends
from typing import Annotated

from app.schemas.auth_schema import Token
from app.schemas.user_schema import UserCreate, User
from app.auth.security import verify_password, create_hashed_password, create_access_token
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app.database.db import Users, get_async_session
from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/auth", tags=["auth"])

async def verify_user(email : str , password : str, session: AsyncSession = Depends(get_async_session)):
    user = await session.execute(select(Users).where(Users.email == email))
    user = user.scalars().first()

    if user is None or not verify_password(password,user.password):
        return None

    return user

@router.post("/login", response_model = Token, status_code=status.HTTP_200_OK)
async def login_user( form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: AsyncSession = Depends(get_async_session)):

    user = await verify_user(form_data.username, form_data.password, session)

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    if user.disabled:
        user.disabled = False
        session.add(user)
        await session.commit()
    
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register", response_model = User, status_code=status.HTTP_200_OK)
async def register_user(
    full_name: str,
    email: str,
    password: str,
    session: AsyncSession = Depends(get_async_session)
):
    
    user = await session.execute(select(Users).where(Users.email == email))
    
    user = user.scalars().first()

    if user:
        raise HTTPException(status_code=400, detail="Email already registered")

    password_hashed = create_hashed_password(password)

    new_user = Users(
        full_name = full_name,
        email = email,
        password = password_hashed,
    )

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return new_user







