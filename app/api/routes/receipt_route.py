from fastapi import APIRouter, Depends
from core.deps import get_current_user
from models.user import ReceiptCreateModel, ReceiptResponseModel, GetUserDataModel
from services.receipt_service import create_receipt

receipt_router = APIRouter()

@receipt_router.post("/", response_model=ReceiptResponseModel)
async def create_receipt_endpoint(receipt: ReceiptCreateModel, current_user: GetUserDataModel = Depends(get_current_user)):
    return await create_receipt(receipt, current_user.id)