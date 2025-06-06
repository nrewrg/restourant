from fastapi import APIRouter, Depends, Response

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from typing import Annotated, Dict, List, Union

from database import get_db_session

from auth import get_current_user, admin

from http_exceptions import AccessDenied

from .models import User
from .schemas import CreateUserSchema, UpdateUserSchema, CreateAdminSchema

from . import service


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", status_code=201, response_model=Dict[str, Union[str, User]])
async def create_user(
    data: CreateUserSchema, db_session: Annotated[AsyncSession, Depends(get_db_session)]
):
    return await service.create(data, db_session)


@router.post("/admin", status_code=201, response_model=Dict[str, Union[str, User]])
async def create_admin_user(
    data: CreateAdminSchema,
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
):
    return await service.create(data, db_session)


@router.get("/{id}", response_model=User)
async def get_user_by_id(
    id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
):
    if current_user.role != "admin":
        if current_user.id != id:
            raise AccessDenied()

    return await service.get(id, db_session)


@router.get("/phone/{phone_number}", response_model=User)
async def get_user_by_phone_number(
    phone_number: str,
    current_user: Annotated[User, Depends(get_current_user)],
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
):
    if current_user.role != "admin":
        if current_user.phone_number != phone_number:
            raise AccessDenied()

    return await service.get_with_phone_number(phone_number, db_session)


@router.get("/current/", response_model=User)
async def get_current_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    return current_user


@router.get("/all/", response_model=List[User])
async def get_all_users(
    current_user: Annotated[User, Depends(admin)],
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
):
    return await service.get_all(db_session)


@router.patch("/{id}", response_model=Dict[str, Union[str, User]])
async def update_user(
    id: int,
    data: UpdateUserSchema,
    current_user: Annotated[User, Depends(get_current_user)],
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
):
    if current_user.role != "admin":
        if current_user.id != id:
            raise AccessDenied()

    return await service.update(id, data, db_session)


@router.delete("/{id}", status_code=204)
async def delete_user(
    id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
):
    if current_user.role != "admin":
        if current_user.id != id:
            raise AccessDenied()

    return await service.delete(id, db_session)
