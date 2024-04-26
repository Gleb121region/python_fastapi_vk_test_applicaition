from datetime import datetime

from pydantic import BaseModel, constr


class NoteBase(BaseModel):
    title: constr(min_length=1, max_length=100)
    content: constr(min_length=1, max_length=1000)


class NoteCreate(NoteBase):
    pass


class NoteUpdate(NoteBase):
    pass


class NoteReadUnauthorized(NoteBase):
    author_login: str


class NoteRead(NoteReadUnauthorized):
    is_owner: bool


class NoteResponse(NoteBase):
    note_id: int
    creation_date: datetime
    author_id: str

    class Config:
        orm_mode = True
