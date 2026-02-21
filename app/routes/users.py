"""
This file contains the routes for the user functionality of the application.
It includes endpoints for creating, retrieving, updating, and deleting users.
"""
from fastapi import APIRouter,HTTPException, status, Depends
from typing import List
from sqlalchemy import select

from app.schemas.user_schema import User, UserCreate, UserUpdate
from app.auth.security import create_hashed_password
from app.database.db import Users
from app.database.db import Notes, get_async_session
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/users", tags=["users"])
"""
    This endpoint allows new users to register by providing their full name, email, and password.
    It checks if the email is already registered, and if not, it creates a new user
"""
@router.post("", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(new_user:UserCreate, session: AsyncSession = Depends(get_async_session)):

    result = await session.execute(select(Users).where(Users.email == new_user.email))
    result = result.scalars().one_or_none()

    if result:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail = "Email already registered")

    password = create_hashed_password(new_user.password)

    user = Users(
        full_name=new_user.full_name,
        email=new_user.email,
        password=password,
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user

"""
    This endpoint allows authenticated users to retrieve a list of all registered users.
    It queries the database for all users and returns them in a list.
"""
@router.get("", response_model=List[User], status_code=status.HTTP_200_OK)
async def get_all_users(session: AsyncSession = Depends(get_async_session)):

    users = await session.execute(select(Users).order_by(Users.created_at.desc()))

    return users.scalars().all()

"""
    This endpoint allows authenticated users to retrieve a specific user by their email.
    It queries the database for a user with the provided email and returns the user if found.
"""
@router.get("/{user_email}", response_model=User, status_code=status.HTTP_200_OK)
async def get_user(user_id: int, session: AsyncSession = Depends(get_async_session)):
    user = await session.execute(select(Users).where(Users.email == user_id))
    user = user.scalars().first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = "User not found")

    return user

"""
    This endpoint allows authenticated users to delete a specific user by their email.
"""
@router.delete("/{user_email}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int , session: AsyncSession = Depends(get_async_session)):
    user = await session.execute(select(Users).where(Users.email == user_id))
    user = user.scalars().first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")

    await session.delete(user)
    await session.commit()

    return
"""
    This endpoint allows authenticated users to update a specific user by their email.
"""
@router.patch("/{user_email}", response_model=User, status_code=status.HTTP_200_OK)
async def update_user(user_id : int, new_user: UserUpdate, session: AsyncSession = Depends(get_async_session)):
    user = await session.execute(select(Users).where(Users.email == user_id))
    user = user.scalars().first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")

    if new_user.email is None and new_user.full_name is None and new_user.password is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Provide at least one update")

    if new_user.email is not None:

        email = await session.execute(select(Users).where(Users.email == new_user.email))

        if not email:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Email already registered")

        user.email = new_user.email


    if new_user.full_name is not None:
        user.full_name = new_user.full_name

    if new_user.password is not None:
        new_password = create_hashed_password(new_user.password)
        user.password_hash = new_password

    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user




