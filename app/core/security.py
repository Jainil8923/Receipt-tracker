from passlib.hash import bcrypt
from jose import jwt
import os

SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-secret-key')

def hash_password(password: str) -> str:
    return bcrypt.hash(password)

def verify_password(password: str, hash: str) -> bool:
    return bcrypt.verify(password, hash)

def create_access_token(payload: dict) -> str:
    try:
        return jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    except Exception as e:
        raise ValueError(f"Token creation failed: {e}")