from db.session import connect, disconnect, prisma
from models.user import ReceiptResponseModel
from fastapi import HTTPException
from typing import List

async def create_receipt(data, user_id):
    try:
        await connect()
        created_receipt = await prisma.receipt.create(
            data={
                "title": data.title,
                "amount": data.amount,
                "category": data.category,
                "date": data.date,
                "user_id": int(user_id)
            }
        )
        return ReceiptResponseModel(
            id=str(created_receipt.id),
            title=created_receipt.title,
            amount=created_receipt.amount,
            category=created_receipt.category,
            date=created_receipt.date,
            user_id=int(user_id),
            updated_at=created_receipt.updated_at,
            created_at=created_receipt.created_at
        )
    except Exception as e:
        print(f"Exception occure in receipt_creation: {e}")
        raise HTTPException(status_code=500, detail="Could not create receipt")
    finally:
        await disconnect()

async def get_user_receipts(user_id: int, skip: int = 0, limit: int = 10) -> List[ReceiptResponseModel]:
    try:
        await connect()
        receipts_list = await prisma.receipt.find_many(
            where={"user_id": int(user_id)},
            skip=skip,
            take=limit
        )
        return [
            ReceiptResponseModel(
                id=str(r.id),
                title=r.title,
                amount=r.amount,
                category=r.category,
                date=r.date,
                user_id=r.user_id,
                updated_at=r.updated_at if hasattr(r, "updated_at") else None,
                created_at=r.created_at
            )
            for r in receipts_list
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail="Could not fetch receipts.")
    finally:
        await disconnect()
        
async def get_receipt_by_id(receipt_id: int) -> ReceiptResponseModel:
    try:
        await connect()
        receipt = await prisma.receipt.find_unique(where={"id":receipt_id})
        if not receipt:
            raise HTTPException(status_code=404, detail="Receipt not found.")
        return ReceiptResponseModel(
                id=str(receipt.id),
                title=receipt.title,
                amount=receipt.amount,
                category=receipt.category,
                date=receipt.date,
                user_id=receipt.user_id,
                updated_at=receipt.updated_at if hasattr(receipt, "updated_at") else None,
                created_at=receipt.created_at
            )
    except Exception as e:
        raise e 
    finally:
        await disconnect()