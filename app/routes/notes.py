from fastapi import APIRouter,HTTPException, status, Depends
from typing import List, Annotated
from sqlalchemy import select
from app.schemas.notes_schema import Note, NoteCreate
from app.database.db import Notes, Users, get_async_session
from app.auth.security import get_current_active_user
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(prefix='/notes', tags=['notes'])
@router.post("", response_model= Note, status_code=status.HTTP_201_CREATED)
async def create_note(
        new_note: NoteCreate,
        current_user: Annotated[Users, Depends(get_current_active_user)],
        session: AsyncSession = Depends(get_async_session),
):
    new_note = Notes(
        title = new_note.title,
        content = new_note.content,
        user_id = current_user.id
    )

    session.add(new_note)
    await session.commit()
    await session.refresh(new_note)
    return new_note

@router.get("", response_model= List[Note] , status_code=status.HTTP_200_OK)
async def get_all_notes(
        session: AsyncSession = Depends(get_async_session),
):

    result = await session.execute(select(Notes).order_by(Notes.id.asc()))

    return result.scalars().all()

@router.get("/{note_id}" , response_model = Note, status_code=status.HTTP_200_OK)
async def get_note(note_id:int, session: AsyncSession = Depends(get_async_session)):

    result = await session.execute(select(Notes).where(Notes.id == note_id))
    note = result.scalars().one_or_none()

    if note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")

    else:
        return note

@router.patch("/{note_id}" , response_model = Note, status_code=status.HTTP_200_OK)
async def update_note(note_id:int, new_note: NoteCreate , session: AsyncSession = Depends(get_async_session)):

    if new_note.title is None or new_note.content is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Title and content are required")

    result = await session.get(Notes, note_id)


    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    else:
        result.title = new_note.title
        result.content = new_note.content
        session.add(result)
        await session.commit()
        await session.refresh(result)

        return result



@router.delete("/{note_id}" , status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(note_id:int, session: AsyncSession = Depends(get_async_session)):

    result = await session.get(Notes,note_id)

    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")

    await session.delete(result)
    await session.commit()

    return








