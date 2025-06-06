from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from sqlalchemy.exc import IntegrityError

from fastapi import HTTPException

from http_exceptions import ObjectWithIdNotFound

from config import settings

from .models import Category
from .schemas import CreateCategorySchema, UpdateCategorySchema


async def create(data: CreateCategorySchema, db_session: AsyncSession):
    """
    Create a new category in the database.

    Args:
        data (CreateCategorySchema): The data required to create a category.
        db_session (AsyncSession): The asynchronous database session.

    Raises:
        HTTPException:
            - 409 if a category with the same slug already exists.

    Returns:
        dict: A dictionary containing a success message and the created category instance.
    """
    category = Category(**data.model_dump())

    try:
        db_session.add(category)
        await db_session.commit()
        await db_session.refresh(category)
    except IntegrityError:
        raise HTTPException(
            status_code=409, detail="Category with this slug already exist"
        )

    return {"message": "Category created", "category": category}


async def get(id: int, db_session: AsyncSession):
    """
    Retrieve a category by its unique ID.

    Args:
        id (int): The ID of the category to retrieve.
        db_session (AsyncSession): The asynchronous database session.

    Raises:
        ObjectWithIdNotFound: If no category with the given ID exists.

    Returns:
        Category: The category instance with the specified ID.
    """
    res = await db_session.exec(select(Category).where(Category.id == id))
    category = res.first()
    if category is None:
        raise ObjectWithIdNotFound(id, Category)
    return category


async def get_with_slug(slug: str, db_session: AsyncSession):
    """
    Retrieve a category by its slug.

    Args:
        slug (str): The slug identifier of the category.
        db_session (AsyncSession): The asynchronous database session.

    Raises:
        HTTPException:
            - 404 if no category with the given slug is found.

    Returns:
        Category: The category instance with the specified slug.
    """
    res = await db_session.exec(select(Category).where(Category.slug == slug))
    category = res.first()
    if category is None:
        raise HTTPException(
            status_code=404, detail=f"Category with slug '{slug}' not found"
        )
    return category


async def get_all(db_session: AsyncSession):
    """
    Retrieve all categories from the database.

    Args:
        db_session (AsyncSession): The asynchronous database session.

    Returns:
        List[Category]: A list of all category instances.
    """
    res = await db_session.exec(select(Category))
    categories = res.all()

    return categories


async def update(
    id: int,
    data: UpdateCategorySchema,
    db_session: AsyncSession,
):
    """
    Update an existing category's information.

    Args:
        id (int): The ID of the category to update.
        data (UpdateCategorySchema): The data to update the category with.
        db_session (AsyncSession): The asynchronous database session.

    Returns:
        dict: A dictionary containing a success message and the updated category instance.
    """
    category = await get(id, db_session)

    for k, v in data.model_dump().items():
        if v is not None:
            setattr(category, k, v)

    db_session.add(category)
    await db_session.commit()
    await db_session.refresh(category)

    return {"message": "Category updated", "category": category}


async def delete(
    id: int,
    db_session: AsyncSession,
):
    """
    Delete a category from the database by its ID.

    Args:
        id (int): The ID of the category to delete.
        db_session (AsyncSession): The asynchronous database session.

    Raises:
        ObjectWithIdNotFound: If no category with the given ID exists.

    Returns:
        None
    """
    category = await get(id, db_session)

    await db_session.delete(category)
    await db_session.commit()
