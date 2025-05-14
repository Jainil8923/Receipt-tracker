from fastapi import APIRouter, Depends, HTTPException
from core.deps import get_current_user
from models.user import GetUserDataModel, UserProfileUpdateModel
from services.user_service import update_user_by_id
from typing import List

user_router = APIRouter()

@user_router.put("/{user_id}", response_model=GetUserDataModel, tags=["User"])
async def update_receipt_by_id_endpoint(user_id: int, payload:UserProfileUpdateModel, current_user: GetUserDataModel = Depends(get_current_user)):
    if str(user_id) != str(current_user.id):
        raise HTTPException(status_code=403, detail="You are not authorized to update this profile.")
    return await update_user_by_id(user_id, payload)

