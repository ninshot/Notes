from fastapi import APIRouter,HTTPException, status
from app.schemas.auth_schema import UserAuth, LoginResponse
from app.auth.security import verify_password

router = APIRouter(prefix="/auth", tags=["auth"])

def verify_user(v_user:UserAuth,)-> bool:
    user = None
    for u in storage.user_db.values():
        if u["email"] == v_user.email:
            user = u
            break

    if user is None or not verify_password(v_user.password,user["password_hash"]):
        return False

    return True



