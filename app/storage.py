
from app.schemas.user_schema import User


def to_public(user_data : dict) -> User:
    return User(
        id = user_data["id"],
        email = user_data["email"],
        full_name = user_data["full_name"],
        created_at = user_data["created_at"],
    )