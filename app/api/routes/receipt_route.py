from fastapi import APIRouter, Depends, HTTPException
from core.deps import get_current_user
from models.user import ReceiptCreateModel, ReceiptResponseModel, GetUserDataModel
from services.receipt_service import create_receipt, get_user_receipts
from typing import List

receipt_router = APIRouter()

@receipt_router.post("/", response_model=ReceiptResponseModel)
async def create_receipt_endpoint(receipt: ReceiptCreateModel, current_user: GetUserDataModel = Depends(get_current_user)):
    return await create_receipt(receipt, current_user.id)

@receipt_router.get("/", response_model=List[ReceiptResponseModel])
async def get_receipts_endpoint(
    skip: int = 0,
    limit: int = 10,
    current_user: GetUserDataModel = Depends(get_current_user)
):
    try:
        return await get_user_receipts(current_user.id, skip, limit)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")
