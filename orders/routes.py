from fastapi import APIRouter, Depends, Response

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from typing import Annotated, Dict, List, Union

from database import get_db_session

from users import User

from auth import get_current_user, admin

from http_exceptions import AccessDenied

from .models import Order, Status

from . import service


router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/", status_code=201, response_model=Dict[str, Union[str, Order]])
async def create_order(
    current_user: Annotated[User, Depends(get_current_user)],
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
):
    return await service.create(current_user.id, db_session)


@router.get("/{id}", response_model=Order)
async def get_order_by_id(
    id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
):
    return await service.get(id, current_user, db_session)


@router.get("/user/{user_id}", response_model=List[Order])
async def get_orders_by_user_id(
    user_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
):
    if current_user.id != user_id:
        if current_user.role != "admin":
            raise AccessDenied()

    return await service.get_with_user_id(user_id, db_session)


@router.get("/user/current/", response_model=List[Order])
async def get_current_user_orders(
    current_user: Annotated[User, Depends(get_current_user)],
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
):
    return await service.get_with_user_id(current_user.id, db_session)


@router.patch("/{id}", response_model=Dict[str, Union[str, Order]])
async def update_order_status(
    id: int,
    status: Status,
    current_user: Annotated[User, Depends(admin)],
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
):
    return await service.update_status(id, status, current_user, db_session)
