from sqlmodel.ext.asyncio.session import AsyncSession

from fastapi import APIRouter, Depends

from typing import Annotated, Dict, Union

from database import get_db_session

from auth import get_current_user

from users import User

from . import service

from .models import Cart


router = APIRouter(prefix="/cart", tags=["Cart"])


@router.get("/", response_model=Cart)
async def get_current_user_cart(
    current_user: Annotated[User, Depends(get_current_user)],
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
):
    return await service.get(current_user.id, db_session)


@router.patch("/add/{product_id}", response_model=Dict[str, Union[str, Cart]])
async def add_product_to_current_user_cart(
    product_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
):
    return await service.add_product(current_user.id, product_id, db_session)


@router.patch("/quantity/{product_id}", response_model=Dict[str, Union[str, Cart]])
async def set_quantity_for_product_in_current_user_cart(
    product_id: int,
    quantity: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
):
    return await service.set_quantity_for_product(
        current_user.id, product_id, quantity, db_session
    )


@router.patch("/remove/{product_id}", response_model=Dict[str, Union[str, Cart]])
async def remove_product_from_current_user_cart(
    product_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
):
    return await service.remove_product(current_user.id, product_id, db_session)
