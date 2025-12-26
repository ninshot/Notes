from fastapi import APIRouter,HTTPException, status
from datetime import datetime
from typing import List

import app.storage as storage
from app.schemas import User, UserCreate
from app.security import create_hashed_password

router = APIRouter(prefix="/users", tags=["users"])

@router.post("", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(new_user:UserCreate):

    for exist_user in storage.user_db.values():
        if exist_user["email"].lower() == new_user.email:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="Email already registered")

    user = {
        "id": storage.user_id,
        "email": new_user.email,
        "full_name": new_user.full_name,
        "password_hash": create_hashed_password(new_user.password),
        "created_at": datetime.utcnow(),
    }
    storage.user_db[user["id"]] = user
    storage.user_id += 1

    storage.save_users()

    return storage.to_public(user)

@router.get("", response_model=List[User], status_code=status.HTTP_200_OK)
async def get_all_users():
    users = storage.user_db.values()
    return users

@router.get("/{user_id}", response_model=User, status_code=status.HTTP_200_OK)
async def get_user(user_id: int):
    if user_id not in storage.user_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")

    user = storage.user_db[user_id]

    return storage.to_public(user)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int):
    if user_id not in storage.user_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")
    del storage.user_db[user_id]
    storage.save_users()

    return None

@router.patch("/{user_id}", response_model=User, status_code=status.HTTP_200_OK)
async def update_user(user_id: int, new_user: UserCreate):
    user = storage.user_db.get(user_id)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")

    if new_user.email is None and new_user.full_name is None and new_user.password is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Provide atleast one update")

    if new_user.email is not None:
        for user_id, user in storage.user_db.items():
            if user["id"] != user_id and user["email"] == new_user.email:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                    detail="Email already registered")

        user["email"] = new_user.email

    if new_user.full_name is not None:
        user["full_name"] = new_user.full_name

    if new_user.password is not None:
        user["password_hash"] = create_hashed_password(new_user.password)

    storage.user_db[user_id] = user
    storage.save_users()

    return storage.to_public(user)




