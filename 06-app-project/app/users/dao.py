from app.dao.base import BaseDAO
from .models import Users


class UserDAO(BaseDAO):
    model = Users
