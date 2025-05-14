from fastapi import APIRouter, HTTPException, Form, Request
from models.user import UserRegistrationModel, UserLoginModel, GetUserDataModel, UserLoginToken, EmailRequest
from core.security import hash_password, verify_password, create_access_token, create_email_verification_token, verify_email_verification_token
from db.session import connect, disconnect, prisma
from prisma.errors import UniqueViolationError
import datetime
import os
from fastapi.responses import JSONResponse
from core.email_utils import send_verification_email

auth_router = APIRouter()

@auth_router.post('/register', response_model=GetUserDataModel, status_code=201, tags=["Auth"])
async def register_user(user: UserRegistrationModel):
    try:
        await connect()
        
        existing = await prisma.user.find_unique(where={"email": user.email})
        if existing:
            raise HTTPException(status_code=409, detail="Email already registered")

        user.password = hash_password(user.password)
        try:
            try:
                verification_data = {"email": user.email}
                token = create_email_verification_token(verification_data)
                await send_verification_email(user.email, token)
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Failed to send verification email: {e}")
            
            created_user = await prisma.user.create(
                data={
                    "name": user.name,
                    "email": user.email,
                    "password": user.password,
                }
            )
        except UniqueViolationError:
            raise HTTPException(status_code=409, detail="Email already registered")
        except Exception as e:
            print(f"Error in email verification or user creation: {e}")
            raise HTTPException(status_code=500, detail="Failed to create user")
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
        

@auth_router.post('/login', response_model=UserLoginToken, status_code=201, tags=["Auth"])
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
            "sub": user_auth.email,
            "iat": datetime.datetime.utcnow(),
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=int(os.getenv("JWT_EXPIRATION_MINUTES", 30)))
        }
        token = create_access_token(payload)
        response = JSONResponse(content={"access_token": user_auth.email,"token": token, "token_type":"bearer"})
        response.set_cookie(
            key="access_token",
            value=token,
            httponly=True,
            secure=True,
            max_age=60*30,
            path="/"
        )
        return {"access_token": token, "token_type": "bearer"}
    except HTTPException as e:
        raise e 
    except Exception as e:
        print(f"Unexpected error in login service: {e}")
        raise HTTPException(status_code=500, detail="Internal server error.")
    finally:
        await disconnect()

@auth_router.post('/token', response_model=UserLoginToken, tags=["Auth"])
async def login_oauth(
    username: str = Form(...),
    password: str = Form(...)
):
    user_auth = UserLoginModel(email=username, password=password)
    return await login(user_auth)

@auth_router.get("/verify-email", tags=["Auth"])
async def verify_email(token: str):
    payload = verify_email_verification_token(token)
    if not payload:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    user_email = payload.get("user_email")
    await connect()
    await prisma.user.update(
        where={"email": user_email},
        data={"is_verified": True}
    )
    await disconnect()
    return {"message": "Email successfully verified!"}

@auth_router.post("/resend-verification", status_code=200, tags=["Auth"])
async def resend_verification_email(payload: EmailRequest):
    email = payload.email

    if not email:
        raise HTTPException(status_code=400, detail="Email is required.")

    await connect()
    user = await prisma.user.find_unique(where={"email": email})
    await disconnect()

    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    if user.is_verified:
        raise HTTPException(status_code=400, detail="User is already verified.")

    token_data = {
        "user_email": user.email,
        "iat": datetime.datetime.utcnow(),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=int(os.getenv("JWT_EXPIRATION_MINUTES", 30)))
    }
    token = create_access_token(token_data)

    await send_verification_email(user.email, token)

    return {"message": "Verification email resent successfully."}
