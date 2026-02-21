"""
This file contains the routes for the notes functionality of the application.
It includes endpoints for creating, retrieving, updating, and deleting notes.
Each endpoint is protected by authentication, ensuring that only registered and logged-in users can access their notes
"""

from fastapi import APIRouter,HTTPException, status, Depends
from typing import List, Annotated
from sqlalchemy import select
from app.schemas.notes_schema import Note, NoteCreate
from app.database.db import Notes, Users, get_async_session
from app.auth.security import get_current_active_user
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(prefix='/notes', tags=['notes'])
"""
    This endpoint allows authenticated users to create a new note by providing a title and content.
    It takes the note data from the request body, associates it with the current user, and saves it to the database.
"""
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

"""
    This endpoint allows authenticated users to retrieve all their notes.
    It queries the database for notes associated with the current user and returns them in a list.
"""
@router.get("", response_model= List[Note] , status_code=status.HTTP_200_OK)
async def get_all_notes(
        current_user: Annotated[Users, Depends(get_current_active_user)],
        session: AsyncSession = Depends(get_async_session),
):

    result = await session.execute(select(Notes).where(Notes.user_id == current_user.id).order_by(Notes.id.asc()))

    return result.scalars().all()
"""
    This endpoint allows authenticated users to retrieve a specific note by its ID.
"""
@router.get("/{note_id}" , response_model = Note, status_code=status.HTTP_200_OK)
async def get_note(note_id:int, 
                   current_user: Annotated[Users, Depends(get_current_active_user)],
                   session: AsyncSession = Depends(get_async_session)):
    
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Register or login to continue")

    result = await session.execute(select(Notes).where(Notes.id == note_id))
    note = result.scalars().one_or_none()

    if note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")

    else:
        return note
"""
    This endpoint allows authenticated users to update a specific note by its ID.
    It takes the updated note data from the request body and updates the corresponding note in the database
"""
@router.patch("/{note_id}" , response_model = Note, status_code=status.HTTP_200_OK)
async def update_note(note_id:int, new_note: NoteCreate ,
                      current_user: Annotated[Users, Depends(get_current_active_user)], 
                      session: AsyncSession = Depends(get_async_session)):

    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Register or login to continue")
    
    if new_note.title is None or new_note.content is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Title and content are required")

    result = await session.get(Notes, note_id)


    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")

    if result.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don't have permission to update this note")
    else:
        result.title = new_note.title
        result.content = new_note.content
        session.add(result)
        await session.commit()
        await session.refresh(result)

        return result


"""
    This endpoint allows authenticated users to delete a specific note by its ID."""
@router.delete("/{note_id}" , status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(note_id:int, 
                      current_user : Annotated[Users, Depends(get_current_active_user)],
                      session: AsyncSession = Depends(get_async_session)):
    
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Register or login to continue")
    
    result = await session.get(Notes,note_id)

    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    if result.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don't have permission to delete this note")

    await session.delete(result)
    await session.commit()

    return








