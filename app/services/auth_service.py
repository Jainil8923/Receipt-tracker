from fastapi import APIRouter, HTTPException
from models.user import UserRegistrationModel, UserLoginModel, GetUserDataModel
from core.security import hash_password, verify_password, create_access_token
from db.session import connect, disconnect, prisma
from prisma.errors import UniqueViolationError

auth_router = APIRouter()

@auth_router.post('/register', response_model=GetUserDataModel, status_code=201)
async def register_user(user: UserRegistrationModel):
    try:
        await connect()
        
        existing = await prisma.user.find_unique(where={"email": user.email})
        if existing:
            raise HTTPException(status_code=409, detail="Email already registered")

        user.password = hash_password(user.password)
        created_user = await prisma.user.create(
            data={
                "name": user.name,
                "email": user.email,
                "password": user.password,
            }
        )
        return GetUserDataModel(
            id=str(created_user.id),
            name=created_user.name,
            email=created_user.email,
            created_at=created_user.created_at,
            updated_at=created_user.updated_at,
            deleted_at=created_user.deleted_at,
            is_verified=created_user.is_verified,
            is_deleted=created_user.is_deleted,
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error occurred in auth_service: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        await disconnect()