from pydantic import BaseModel, EmailStr, Field
from enum import Enum
from datetime import datetime


class UserRole(str, Enum):
    customer = "customer"
    admin = "admin"


class UserCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6)
    

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserCreateResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: UserRole
    created_at: datetime

    class Config:
        from_attributes = True

from typing import List

class UserListResponse(BaseModel):
    users: List[UserCreateResponse]
    total: int
    skip: int
    limit: int

from typing import Optional
class UserUpdate(BaseModel):
    name: Optional[str] = None
    password: Optional[str] = None

class MessageResponse(BaseModel):
    message: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenPayload(BaseModel):
    sub: str | None = None