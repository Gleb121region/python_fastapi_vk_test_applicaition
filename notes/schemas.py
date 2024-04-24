from datetime import datetime

from pydantic import BaseModel


class NoteCreate(BaseModel):
    title: str
    content: str


class NoteUpdate(BaseModel):
    title: str
    content: str


class NoteResponse(BaseModel):
    note_id: int
    title: str
    content: str
    creation_date: datetime
    author_id: str

    class Config:
        orm_mode = True
