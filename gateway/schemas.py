from typing import Optional

from pydantic import EmailStr, BaseModel


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
    is_own: bool
