from fastapi import APIRouter, Depends, Response

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from typing import Annotated, Dict, List, Union

from database import get_db_session

from users import User

from auth import admin

from .models import Category
from .schemas import CreateCategorySchema, UpdateCategorySchema

from . import service


router = APIRouter(prefix="/categories", tags=["Categories"])


@router.post("/", status_code=201, response_model=Dict[str, Union[str, Category]])
async def create_category(
    data: CreateCategorySchema,
    current_user: Annotated[User, Depends(admin)],
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
):
    return await service.create(data, db_session)


@router.get("/{id}", response_model=Category)
async def get_category_by_id(
    id: int,
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
):
    return await service.get(id, db_session)


@router.get("/slug/{slug}", response_model=Category)
async def get_category_by_slug(
    slug: str,
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
):
    return await service.get_with_slug(slug, db_session)


@router.get("/all/", response_model=List[Category])
async def get_all_categories(
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
):
    return await service.get_all(db_session)


@router.patch("/{id}", response_model=Dict[str, Union[str, Category]])
async def update_category(
    id: int,
    data: UpdateCategorySchema,
    current_user: Annotated[User, Depends(admin)],
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
):
    return await service.update(id, data, db_session)


@router.delete("/{id}", status_code=204)
async def delete_category(
    id: int,
    current_user: Annotated[User, Depends(admin)],
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
):
    return await service.delete(id, db_session)
