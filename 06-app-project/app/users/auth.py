from passlib.context import CryptContext
from sqlalchemy.util import deprecated
from pydantic import EmailStr
from fastapi import HTTPException, status
from datetime import datetime, timedelta
from jose import jwt
from app.config import settings
from app.exceptions import UserNotFoundException

from app.users.dao import UserDAO

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=60)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, settings.ALGORITHM
    )

    return encoded_jwt



async def authenticate_user(email: EmailStr, password: str):
    user = await UserDAO.find_one_or_none(email=email)
    if not user:
        raise UserNotFoundException
    if not verify_password(password, user.password):
        return None
    return user