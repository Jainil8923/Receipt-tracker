from pydantic import BaseModel 
from pydantic_extra_types.pendulum_dt import Date
from typing import Optional
from datetime import datetime

class UserRegistrationModel(BaseModel):
    name: str 
    email: str 
    password: str 

class UserLoginModel(BaseModel):
    email: str 
    password: str 

class GetUserDataModel(BaseModel):
    id: str
    name: str
    email: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    is_verified: bool
    is_deleted: bool