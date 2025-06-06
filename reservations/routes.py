from sqlmodel.ext.asyncio.session import AsyncSession

from fastapi import APIRouter, Depends

from typing import Annotated, Dict, List, Union

from database import get_db_session

from auth import get_current_user, admin

from http_exceptions import AccessDenied

from users import User

from . import service
from .models import Reservation

router = APIRouter(prefix="/reservations", tags=["Reservations"])


@router.post("/", status_code=201, response_model=Dict[str, Union[str, Reservation]])
async def create_reservation(
    time: str,
    current_user: Annotated[User, Depends(get_current_user)],
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
):
    return await service.create(time, current_user.id, db_session)


@router.get("/{id}", response_model=Reservation)
async def get_reservation_by_id(
    id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
):
    return await service.get(id, current_user, db_session)


@router.get("/user/{user_id}", response_model=List[Reservation])
async def get_reservations_by_user_id(
    user_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
):
    if current_user.id != user_id:
        if current_user.role != "admin":
            raise AccessDenied()

    return await service.get_by_user_id(user_id, db_session)


@router.get("/user/current/", response_model=List[Reservation])
async def get_current_user_reservations(
    current_user: Annotated[User, Depends(get_current_user)],
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
):
    return await service.get_by_user_id(current_user.id, db_session)


@router.get("/all/", response_model=List[Reservation])
async def get_all_reservations(
    current_user: Annotated[User, Depends(admin)],
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
):
    return await service.get_all(db_session)


@router.delete("/", status_code=204)
async def delete_reservation(
    id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
):
    return await service.delete(id, db_session)
