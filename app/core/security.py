from passlib.hash import bcrypt
from jose import jwt, JWTError, ExpiredSignatureError
import os
from fastapi import HTTPException
from dotenv import load_dotenv
import datetime 

load_dotenv()


SECRET_KEY = os.getenv('SECRET_KEY')
if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable is not set.")
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
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")

def create_email_verification_token(data: dict, expires_minutes: int = 1440):
    expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=expires_minutes)
    to_encode = {**data, "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_email_verification_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except:
        return None
