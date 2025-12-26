from fastapi import APIRouter,HTTPException, status
import app.storage as storage
from app.schemas import UserAuth, LoginResponse
from app.security import verify_password

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
def verify_user(v_user:UserAuth):
    user = None
    for u in storage.user_db.values():
        if u["email"] == v_user.email:
            user = u
            break

    if user is None or not verify_password(v_user.password,user["password_hash"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect email or password",)

    return LoginResponse(message="Login successful",
                         user_id=user["id"])


