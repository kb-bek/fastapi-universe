from fastapi import Depends
from starlette.requests import Request
from jose import jwt, JWTError
from datetime import datetime

from app.config import settings
from app.exceptions import ExpiredTokenException, MissingTokenException, JWTErrorException, MissingUserIDException, \
    UserNotFoundException
from app.users.dao import UserDAO


def get_token(request: Request):
    token = request.cookies.get("booking_access_token")
    if not token:
        raise MissingTokenException
    return token

async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, settings.ALGORITHM
        )
    except JWTError:
        raise JWTErrorException

    expire: str = payload.get("exp")
    if (not expire) or (int(expire) < datetime.utcnow().timestamp()):
        raise ExpiredTokenException

    user_id: str = payload.get("sub")
    if not user_id:
        raise MissingUserIDException

    user = await UserDAO.find_by_id(int(user_id))
    if not user:
        raise UserNotFoundException

    return user
