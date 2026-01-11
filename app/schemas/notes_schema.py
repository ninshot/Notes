from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class NoteCreate(BaseModel):
    title:str = Field(min_length=1,max_length=100)
    content:str = Field(min_length=1,max_length=100)

class Note(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    content: str
    created_at: datetime
