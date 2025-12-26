import json
from app.schemas import Note, User
from pathlib import Path
from datetime import datetime
from typing import Dict, Tuple

notes_db : Dict[int,Note] = {}
next_id = 1
user_db : Dict[int,dict]  = {}
user_id = 1

DIR = Path(__file__).resolve().parent

DATA_PATH = DIR / "data"/"notes.json"
USERS_PATH = DIR / "data"/"users.json"

def _note_to_dict(note : Note) -> Dict:
    return {
        "id": note.id,
        "title": note.title,
        "content": note.content,
        "created_at": note.created_at.isoformat(),
        "user_id": note.user_id,
    }

def _dict_to_note(note : Dict) -> Note:
    return Note(
        id = note["id"],
        title = note["title"],
        content = note["content"],
        created_at = datetime.fromisoformat(note["created_at"]),
        user_id = note["user_id"],
    )

def load_notes() -> Tuple[Dict[int,Note],int]:
    global notes_db, next_id, user_db, user_id

    if not DATA_PATH.exists():
        notes_db = {}
        next_id = 1
        return notes_db, next_id

    raw_data = json.loads(DATA_PATH.read_text(encoding="utf-8") or "{}")

    items = raw_data.get("notes",[])

    loaded : Dict[int,Note] = {}
    max_id = 0
    for item in items:
        note = _dict_to_note(item)
        loaded[note.id] = note
        max_id = max(max_id, note.id)

    notes_db = loaded
    next_id = max_id+1
    return notes_db, next_id

def save_notes() -> None:

    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        "notes" : [_note_to_dict(notes_db[k]) for k in sorted(notes_db.keys())]
    }
    DATA_PATH.write_text(json.dumps(payload, indent = 2), encoding="utf-8")

def load_users() -> Tuple[Dict[int,Dict],int]:
    global user_db, user_id

    if not USERS_PATH.exists():
        user_db = {}
        user_id = 1
        return user_db, user_id

    user_data = json.loads(USERS_PATH.read_text(encoding="utf-8") or "{}")
    max_id = 0
    items = user_data.get("users",[])

    new_dict : dict[int,dict] = {}

    for user in items:
        user_id = int(user["id"])
        new_dict[user_id] = {
            "id": user_id,
            "email": user["email"],
            "full_name": user["full_name"],
            "password_hash" : user["password_hash"],
            "created_at": datetime.fromisoformat(user["created_at"]),
        }
        max_id = max(max_id, user_id)

    user_db = new_dict
    user_id = max_id+1
    return user_db, user_id

def save_users() -> None:
    USERS_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "users" : [
            {
                "id": user_db[k]["id"],
                "email" : user_db[k]["email"],
                "full_name" : user_db[k]["full_name"],
                "password_hash" : user_db[k]["password_hash"] ,
                "created_at" : user_db[k]["created_at"].isoformat(),
            }
            for k in sorted(user_db.keys())
        ]
    }

    USERS_PATH.write_text(json.dumps(payload, indent = 2), encoding="utf-8")

def to_public(user_data : dict) -> User:
    return User(
        id = user_data["id"],
        email = user_data["email"],
        full_name = user_data["full_name"],
        created_at = user_data["created_at"],
    )