from fastapi import APIRouter, Depends
from core.deps import get_current_user
from models.user import GetUserDataModel

router = APIRouter()

@router.get("/me", response_model=GetUserDataModel)
async def read_users_me(current_user: GetUserDataModel = Depends(get_current_user)):
    print("hi")
    return current_user
