from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


# 创建请求体
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    age: Optional[int] = None


# 更新请求体
class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    age: Optional[int] = None


# 响应体
class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    age: Optional[int]
    created_at: str

    class Config:
        from_attributes = True
