from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

class UserRegistrationModel(BaseModel):
    name: str = Field(..., max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8)

class UserLoginModel(BaseModel):
    email: EmailStr
    password: str

class GetUserDataModel(BaseModel):
    id: str
    name: str
    email: EmailStr
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    is_verified: bool
    is_deleted: bool