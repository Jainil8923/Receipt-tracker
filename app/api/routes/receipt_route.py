from fastapi import APIRouter, Depends, HTTPException
from core.deps import get_current_user
from models.user import ReceiptCreateModel, ReceiptResponseModel, GetUserDataModel
from services.receipt_service import create_receipt, get_user_receipts, get_receipt_by_id, update_receipt_by_id, delete_receipt_by_id
from typing import List

receipt_router = APIRouter()

@receipt_router.post("/", response_model=ReceiptResponseModel, tags=["Receipt"])
async def create_receipt_endpoint(receipt: ReceiptCreateModel, current_user: GetUserDataModel = Depends(get_current_user)):
    return await create_receipt(receipt, current_user.id)

@receipt_router.get("/", response_model=List[ReceiptResponseModel], tags=["Receipt"])
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

@receipt_router.get("/{receipt_id}", response_model=ReceiptResponseModel, tags=["Receipt"])
async def get_receipt_by_id_endpoint(receipt_id: int, current_user: GetUserDataModel = Depends(get_current_user)):
    receipt = await get_receipt_by_id(receipt_id)
    if str(receipt.user_id) != str(current_user.id):
        raise HTTPException(status_code=403, detail="You are not authorized to access this receipt.")

    return receipt

@receipt_router.put("/{receipt_id}", response_model=ReceiptResponseModel, tags=["Receipt"])
async def update_receipt_by_id_endpoint(receipt_id: int, payload:ReceiptCreateModel, current_user: GetUserDataModel = Depends(get_current_user)):
    receipt = await get_receipt_by_id(receipt_id)
    if str(receipt.user_id) != str(current_user.id):
        raise HTTPException(status_code=403, detail="You are not authorized to access this receipt.")
    return await update_receipt_by_id(receipt_id, payload)
    

@receipt_router.delete("/{receipt_id}", response_model=str, tags=["Receipt"])
async def delete_receipt_by_id_endpoint(receipt_id: int, current_user: GetUserDataModel = Depends(get_current_user)):
    receipt = await get_receipt_by_id(receipt_id)
    if str(receipt.user_id) != str(current_user.id):
        raise HTTPException(status_code=403, detail="You are not authorized to access this receipt.")
    return await delete_receipt_by_id(receipt_id)