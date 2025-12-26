import json
from app.schemas import Note
from pathlib import Path
from datetime import datetime
from typing import Dict, Tuple

notes_db : Dict[int,Note] = {}
next_id = 1

DIR = Path(__file__).resolve().parent

DATA_PATH = DIR / "data"/"notes.json"

def _note_to_dict(note : Note) -> Dict:
    return {
        "id": note.id,
        "title": note.title,
        "content": note.content,
        "created_at": note.created_at.isoformat(),
    }

def _dict_to_note(note : Dict) -> Note:
    return Note(
        id = note["id"],
        title = note["title"],
        content = note["content"],
        created_at = datetime.fromisoformat(note["created_at"]),
    )

def load_notes() -> Tuple[Dict[int,Note],int]:
    global notes_db, next_id

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

