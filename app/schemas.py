from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime

class NoteCreate(BaseModel):
    title:str = Field(min_length=1,max_length=100)
    content:str = Field(min_length=1,max_length=100)
    user_id: int

class Note(NoteCreate):
    id: int
    created_at: datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str

class User(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    created_at: datetime

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str]
    password: Optional[str]

class UserAuth(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    message: str
    user_id: int