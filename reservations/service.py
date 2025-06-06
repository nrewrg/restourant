from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from fastapi import HTTPException

from datetime import datetime, timedelta

from typing import Optional

from users import User

from http_exceptions import ObjectWithIdNotFound, AccessDenied

from .models import Reservation


async def create(time: str, user_id: int, db_session: AsyncSession):
    """
    Create a new reservation for a user at a specified time.

    Args:
        time (str): The reservation time in ISO 8601 format.
        user_id (int): The ID of the user making the reservation.
        db_session (AsyncSession): The asynchronous database session.

    Raises:
        HTTPException:
            - 400 if the reservation time is less than 24 hours from now.

    Returns:
        dict: A dictionary containing a success message and the created reservation instance.
    """
    time = datetime.fromisoformat(time)
    now = datetime.now()

    if time <= now + timedelta(hours=24):
        raise HTTPException(
            status_code=400, detail="Less than 24 hours left until the reservation time"
        )

    reservation = Reservation(user_id=user_id, time=time)

    db_session.add(reservation)
    await db_session.commit()
    await db_session.refresh(reservation)

    return {"message": "Reservation created", "reservation": reservation}


async def get(id: int, current_user: User, db_session: AsyncSession):
    """
    Retrieve a reservation by its ID, enforcing access control.

    Args:
        id (int): The ID of the reservation to retrieve.
        current_user (User): The user requesting the reservation.
        db_session (AsyncSession): The asynchronous database session.

    Raises:
        ObjectWithIdNotFound: If no reservation with the given ID exists.
        AccessDenied: If the current user is neither the owner of the reservation nor an admin.

    Returns:
        Reservation: The reservation instance with the specified ID.
    """
    res = await db_session.exec(select(Reservation).where(Reservation.id == id))
    reservation = res.first()
    if reservation is None:
        raise ObjectWithIdNotFound(id, Reservation)

    if current_user.id != reservation.user_id:
        if current_user.role != "admin":
            raise AccessDenied()

    return reservation


async def get_by_user_id(user_id: int, db_session: AsyncSession):
    """
    Retrieve all reservations for a specific user.

    Args:
        user_id (int): The ID of the user whose reservations to retrieve.
        db_session (AsyncSession): The asynchronous database session.

    Returns:
        List[Reservation]: A list of reservations belonging to the specified user.
    """
    res = await db_session.exec(
        select(Reservation).where(Reservation.user_id == user_id)
    )
    reservations = res.all()

    return reservations


async def get_all(db_session: AsyncSession):
    """
    Retrieve all reservations in the system.

    Args:
        db_session (AsyncSession): The asynchronous database session.

    Returns:
        List[Reservation]: A list of all reservation instances.
    """
    res = await db_session.exec(select(Reservation))
    reservations = res.all()

    return reservations


async def delete(id: int, current_user: User, db_session: AsyncSession):
    """
    Delete a reservation by its ID, enforcing access control.

    Args:
        id (int): The ID of the reservation to delete.
        current_user (User): The user requesting the deletion.
        db_session (AsyncSession): The asynchronous database session.

    Raises:
        ObjectWithIdNotFound: If no reservation with the given ID exists.
        AccessDenied: If the current user is neither the owner of the reservation nor an admin.

    Returns:
        None
    """
    reservation = await get(id, current_user, db_session)

    await db_session.delete(reservation)
    await db_session.commit()
