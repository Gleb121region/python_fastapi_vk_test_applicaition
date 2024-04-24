import re
import uuid
from typing import Optional

from fastapi_users import schemas
from pydantic import EmailStr, Field
from pydantic import validator


class UserRead(schemas.BaseUser[uuid.UUID]):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    email: EmailStr
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    class Config:
        orm_mode = True


class UserCreate(schemas.BaseUserCreate):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False

    @validator("password")
    def password_must_contain_special_characters(cls, v):
        if not re.search("[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search("[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search("[0-9]", v):
            raise ValueError("Password must contain at least one digit")
        return v


class UserUpdate(schemas.BaseUserUpdate):
    password: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None
    is_verified: Optional[bool] = None
