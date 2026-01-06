
from app.schemas.user_schema import User
from app.schemas.notes_schema import Note
from typing import Dict

notes_db : Dict[int,Note] = {}
next_id = 1
user_db : Dict[int,dict]  = {}
user_id = 1

def to_public(user_data : dict) -> User:
    return User(
        id = user_data["id"],
        email = user_data["email"],
        full_name = user_data["full_name"],
        created_at = user_data["created_at"],
    )