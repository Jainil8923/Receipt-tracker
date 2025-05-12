from fastapi import APIRouter, Depends
from core.deps import get_current_user
from models.user import ReceiptCreateModel, ReceiptResponseModel, GetUserDataModel
from services.receipt_service import create_receipt, get_user_receipts
from typing import List

receipt_router = APIRouter()

@receipt_router.post("/", response_model=ReceiptResponseModel)
async def create_receipt_endpoint(receipt: ReceiptCreateModel, current_user: GetUserDataModel = Depends(get_current_user)):
    return await create_receipt(receipt, current_user.id)

@receipt_router.get("/", response_model=List[ReceiptResponseModel])
async def get_receipts_endpoint(current_user:GetUserDataModel = Depends(get_current_user)):
    return await get_user_receipts(current_user.id)