from passlib.hash import bcrypt
from jose import jwt
import os

def hash_password(password: str) -> str:
    return bcrypt.hash(password)

def verify_password(password: str, hash: str)-> bool:
    return bcrypt.verify(password, hash)

def create_access_token(payload: object)-> str:
    return jwt.encode(payload, os.getenv('SECRET_KEY'), algorithm='HS256')
