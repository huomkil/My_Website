from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UserCreate(BaseModel):
    user_phone: str
    user_password: str
    user_name: str
    user_email: EmailStr
    user_age: Optional[int] = None
    user_level: int = 1
    user_tag: Optional[str] = None


class UserUpdate(BaseModel):
    user_name: Optional[str] = None
    user_email: Optional[EmailStr] = None
    user_phone: Optional[str] = None
    user_age: Optional[int] = None
    user_level: Optional[int] = None
    user_tag: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    user_id: str
    user_phone: str
    user_name: str
    user_level: int
    user_tag: Optional[str]
    user_email: str
    user_age: Optional[int]

    class Config:
        from_attributes = True
