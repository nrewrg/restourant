from fastapi import APIRouter, Depends, Response

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from typing import Annotated, Dict, List, Union

from database import get_db_session

from auth import admin

from users import User


from .models import Product
from .schemas import CreateProductSchema, UpdateProductSchema

from . import service


router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/", status_code=201, response_model=Dict[str, Union[str, Product]])
async def create_product(
    data: CreateProductSchema,
    current_user: Annotated[AsyncSession, Depends(admin)],
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
):
    return await service.create(data, db_session)


@router.get("/{id}", response_model=Product)
async def get_product_by_id(
    id: int,
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
):
    return await service.get(id, db_session)


@router.get("/category/{category_slug}", response_model=List[Product])
async def get_products_by_category_slug(
    category_slug: str,
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
):
    return await service.get_with_category_slug(category_slug, db_session)


@router.get("/all/", response_model=List[Product])
async def get_all_products(
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
):
    return await service.get_all(db_session)


@router.patch("/{id}", response_model=Dict[str, Union[str, Product]])
async def update_product(
    id: int,
    data: UpdateProductSchema,
    current_user: Annotated[User, Depends(admin)],
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
):
    return await service.update(id, data, db_session)


@router.delete("/{id}", status_code=204)
async def delete_product(
    id: int,
    current_user: Annotated[User, Depends(admin)],
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
):
    return await service.delete(id, db_session)
