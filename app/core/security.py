from passlib.hash import bcrypt
from jose import jwt, JWTError, ExpiredSignatureError
import os
from fastapi import HTTPException

SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-secret-key')
ALGORITHM = "HS256"


def hash_password(password: str) -> str:
    return bcrypt.hash(password)

def verify_password(password: str, hash: str) -> bool:
    return bcrypt.verify(password, hash)
    
def create_access_token(payload: dict) -> str:
    try:
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    except Exception as e:
        raise ValueError(f"Token creation failed: {e}")

def decode_access_token(token: str) -> dict:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")