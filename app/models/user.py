from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional
from enum import Enum
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

class UserLoginToken(BaseModel):
    access_token: str = Field(..., min_length=20, description="The JWT access token for authentication.")
    token_type: str = Field(..., description="The type of token, usually 'bearer'.")

class ReceiptCategory(str, Enum):
    FOOD = "Food"
    TRANSPORT = "Transport"
    ENTERTAINMENT = "Entertainment"
    OTHER = "Other"

category: ReceiptCategory
class ReceiptCreateModel(BaseModel):
    title: str   
    amount: float = Field(..., gt=0, description="Amount must be greater than zero")
    category: ReceiptCategory
    date: datetime
    updated_at: Optional[datetime] = None

class ReceiptResponseModel(BaseModel):
    id: str
    title: str   
    amount: float
    category: str
    date: datetime
    user_id: int
    updated_at: Optional[datetime] = None
    created_at : datetime
    
class UserProfileUpdateModel(BaseModel):
    name: str = Field(..., max_length=100, pattern="^[a-zA-Z ]+$")
    email: EmailStr
class EmailRequest(BaseModel):
    email: str
