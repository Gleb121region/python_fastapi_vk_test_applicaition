from datetime import datetime
from typing import Optional

from pydantic import BaseModel, constr
from pydantic import EmailStr


class UserRegistration(BaseModel):
    email: EmailStr
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = True


class UserAuthorization(BaseModel):
    username: EmailStr
    password: str


class UserForgotPassword(BaseModel):
    email: EmailStr


class UserResetPassword(BaseModel):
    token: str
    password: str


class UserRequestVerifyToken(BaseModel):
    email: EmailStr


class UserVerifyToken(BaseModel):
    token: str


class UserPatch(BaseModel):
    password: str
    email: EmailStr
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = True


class NoteBase(BaseModel):
    title: constr(max_length=100)
    content: constr(max_length=1000)


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
