from datetime import date

from fastapi import Depends
from app.database import async_session_maker, engine
from sqlalchemy import select, and_, or_, func, insert
from .models import Bookings
from app.dao.base import BaseDAO
from ..hotels.models import Rooms
from ..users.dependencies import get_current_user
from ..users.models import Users


class BookingDAO(BaseDAO):

    model = Bookings

    """
    WITH booked_rooms AS (
        SELECT * FROM bookings
        WHERE room_id = 1 AND 
        (date_from >= '2025-02-10' AND date_from <= '2025-03-10') OR
        (date_from <= '2025-02-10' AND date_to > '2025-05-15')
    )
    
    SELECT rooms.quantity - COUNT(booked_rooms.room_id)  FROM rooms
    LEFT JOIN booked_rooms ON booked_rooms.room_id = rooms.id
    WHERE rooms.id = 1
    GROUP BY rooms.quantity, booked_rooms.room_id
    """

    @classmethod
    async def add(
            cls,
            user_id: int,
            room_id: int,
            date_from: date,
            date_to:date,
    ):
        async with async_session_maker() as session:
            booked_rooms = select(Bookings).where(
                and_(
                    Bookings.room_id == room_id,
                    or_(
                        and_(
                            Bookings.date_from >= date_from,
                            Bookings.date_from <= date_to
                        ),
                        and_(
                            Bookings.date_from <= date_from,
                            Bookings.date_to > date_from
                        )
                    )
                )
            ).cte("booked_rooms")

            get_rooms_left = select(
                (Rooms.quantity - func.count(booked_rooms.c.room_id)).label("rooms_left")
                ).select_from(Rooms).join(
                    booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True
                ).where(Rooms.id == room_id).group_by(
                Rooms.quantity, booked_rooms.c.room_id
            )

            # print(get_rooms_left.compile(engine, compile_kwargs={"literal_blinds": True}))
            rooms_left = await session.execute(get_rooms_left)
            rooms_left:int = rooms_left.scalar()

            if rooms_left > 0:
                get_price = select(Rooms.price).filter_by(id=room_id)
                price = await session.execute(get_price)
                price: int = price.scalar()
                new_booking_query = insert(Bookings).values(
                    room_id=room_id,
                    user_id=user_id,
                    date_from=date_from,
                    date_to=date_to,
                    price=price
                ).returning(Bookings)
                new_booking = await session.execute(new_booking_query)
                await session.commit()
                return new_booking.scalar()
            else:
                return None