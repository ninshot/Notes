from datetime import timedelta, datetime, timezone
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette import status

from sqlalchemy import select
from app.database.db import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.auth_schema import TokenData
from .config import ALGORITHM,SECRET_KEY,ACCESS_TOKEN_EXPIRE_MINUTES

import bcrypt
import jwt
from jwt.exceptions import InvalidTokenError

from ..schemas.user_schema import User
from app.database.db import Users

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
"""
This fucntion is used for creation of a hashed password using bcrypt library.
It generates a salt and hashesthe passowrd using the salt and returns the hashed password as a string.
"""
def create_hashed_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_password.decode("utf-8")
"""
This fucntion is used for verifying the password by comparing
the plain password with the hashed password using bcrypt library.
It returns True if the password is correct, otherwise False.
"""
def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))

"""
This fucntion is used for creating a JWT access token. 
It takes a dictionary of data and an optional expiration time.
"""
def create_access_token(
        data: dict,
        expires_delta: timedelta | None = None):
    
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

"""
This async function is used for getting the current user from the JWT token.
It decodes the token, extracts the email, and retrieves the user from the database.
"""
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)] ,
                           session: AsyncSession = Depends(get_async_session)):
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if not email:
            raise credentials_exception
        token_data = TokenData(email=email)

    except InvalidTokenError:
        raise credentials_exception

    user = await session.execute(select(Users).where(Users.email == token_data.email))
    user = user.scalars().one_or_none()

    if user is None:
        raise credentials_exception

    return user

async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):

    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")

    return current_user









