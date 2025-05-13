from db.session import connect, disconnect, prisma
from models.user import GetUserDataModel, UserProfileUpdateModel
from fastapi import HTTPException
from typing import List
import datetime

async def update_user_by_id(user_id: int, new_user: UserProfileUpdateModel) -> GetUserDataModel:
    try:
        await connect()
        user = await prisma.user.find_unique(where={"id": user_id, "deleted_at": None})
        if not user:
            raise HTTPException(status_code=404, detail="User not found.")
        
        result = await prisma.user.update(
            data={
                **new_user.model_dump(),
            },
            where={"id": int(user_id)}
        )
        return GetUserDataModel(
            id=str(result.id),
            email=result.email,
            name=result.name,
            created_at=result.created_at,
            updated_at=result.updated_at,
            deleted_at=result.deleted_at,
            is_verified=result.is_verified,
            is_deleted=result.is_deleted,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")
    finally:
        await disconnect()
    