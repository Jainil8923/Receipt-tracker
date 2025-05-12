from db.session import connect, disconnect, prisma
from models.user import ReceiptResponseModel
from fastapi import HTTPException

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