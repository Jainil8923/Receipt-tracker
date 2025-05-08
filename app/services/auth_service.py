from fastapi import APIRouter, HTTPException
from models.user import UserRegistrationModel, UserLoginModel, GetUserDataModel, UserLoginToken
from core.security import hash_password, verify_password, create_access_token
from db.session import connect, disconnect, prisma
from prisma.errors import UniqueViolationError
import datetime
import os

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
        raise HTTPException(status_code=500, detail="Internal server error, service = register")
    finally:
        await disconnect()
        
@auth_router.post('/login', response_model=UserLoginToken, status_code=201)
async def login(user_auth: UserLoginModel):
    try:
        await connect()
        existing = await prisma.user.find_first(where={"email": user_auth.email})
        if not existing:
            raise HTTPException(status_code=404, detail="User does not exist.")

        is_password_correct = verify_password(user_auth.password, existing.password)
        if not is_password_correct:
            raise HTTPException(status_code=401, detail="Invalid credentials.")
        payload = {
            "user_email": user_auth.email,
            "iat": datetime.datetime.utcnow(),
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=int(os.getenv("JWT_EXPIRATION_MINUTES", 30)))
        }
        token = create_access_token(payload)
        return {"token": token}

    except HTTPException as e:
        raise e 
    except Exception as e:
        print(f"Unexpected error in login service: {e}")
        raise HTTPException(status_code=500, detail="Internal server error.")
    finally:
        await disconnect()     
