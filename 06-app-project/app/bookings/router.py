from datetime import date

from fastapi import APIRouter, Depends
from typing import List
from app.bookings.dao import BookingDAO
from .schemas import SBookings
from ..exceptions import RoomCannotBeBooked
from ..users.dependencies import get_current_user
from ..users.models import Users

router = APIRouter(
    prefix="/bookings",
    tags=["Booking"]
)

@router.get("")
async def get_bookings(user: Users = Depends(get_current_user)):
    print(user, type(user), user.email)
    return await BookingDAO.find_all(user_id=user.id)

@router.post("")
async def add_booking(
    room_id: int, date_from: date, date_to:date,
    user: Users = Depends(get_current_user)
):
    booking = await BookingDAO.add(user.id, room_id, date_from, date_to)
    if not booking:
        raise RoomCannotBeBooked