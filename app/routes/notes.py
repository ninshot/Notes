from fastapi import APIRouter,HTTPException, status
from datetime import datetime
from typing import List

import app.storage as storage
from app.schemas import Note, NoteCreate


router = APIRouter(prefix='/notes', tags=['notes'])
@router.post("", response_model= Note, status_code=status.HTTP_201_CREATED)
async def create_note(new_note: NoteCreate):

    note = Note(
        id = storage.next_id,
        title = new_note.title,
        content = new_note.content,
        created_at = datetime.utcnow(),
    )
    storage.notes_db[note.id] = note
    storage.next_id +=1

    storage.save_notes()
    return note

@router.get("", response_model = List[Note], status_code=status.HTTP_200_OK)
async def get_all_notes():
    res = []

    for value in storage.notes_db.values():
        res.append(value)

    return res

@router.get("/{note_id}" , response_model = Note, status_code=status.HTTP_200_OK)
async def get_note(note_id:int):

    if note_id not in storage.notes_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Note not found")

    return storage.notes_db[note_id]

@router.patch("/{note_id}" , response_model = Note, status_code=status.HTTP_200_OK)
async def update_note(note_id:int, new_note: NoteCreate):

    if note_id not in storage.notes_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Note not found")

    if new_note.title is None or new_note.content is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Title and content are required")

    old_note = storage.notes_db[note_id]
    old_note.title = new_note.title
    old_note.content = new_note.content
    storage.notes_db[note_id] = old_note
    storage.save_notes()
    return storage.notes_db[note_id]

@router.delete("/{note_id}" , status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(note_id:int):
    if note_id not in storage.notes_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Note not found")
    del storage.notes_db[note_id]

    storage.save_notes()
    return None








