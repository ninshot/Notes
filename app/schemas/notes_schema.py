from pydantic import BaseModel, Field
from datetime import datetime

class NoteCreate(BaseModel):
    title:str = Field(min_length=1,max_length=100)
    content:str = Field(min_length=1,max_length=100)

class Note(NoteCreate):
    id: int
    created_at: datetime