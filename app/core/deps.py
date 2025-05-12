from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from core.security import decode_access_token
from models.user import GetUserDataModel
from db.session import connect, disconnect, prisma

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> GetUserDataModel:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token)
        user_email: str = payload.get("sub")
        if user_email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    async with prisma as db:
        user = await db.user.find_first(where={"email": user_email})
    if user is None:
        raise credentials_exception
    return GetUserDataModel(
        id=str(user.id),
        name=user.name,
        email=user.email,
        created_at=user.created_at,
        updated_at=user.updated_at,
        deleted_at=user.deleted_at,
        is_verified=user.is_verified,
        is_deleted=user.is_deleted,
    )
