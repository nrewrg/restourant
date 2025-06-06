from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from sqlalchemy.exc import IntegrityError

from fastapi import HTTPException

from http_exceptions import ObjectWithIdNotFound

from categories import service as categories_service

from config import settings

from .models import Product
from .schemas import CreateProductSchema, UpdateProductSchema


async def create(data: CreateProductSchema, db_session: AsyncSession):
    """
    Create a new product in the database.

    Args:
        data (CreateProductSchema): The data required to create a product.
        db_session (AsyncSession): The asynchronous database session.

    Raises:
        HTTPException:
            - 400 if the referenced category_id does not exist.

    Returns:
        dict: A dictionary containing a success message and the created product instance.
    """
    product = Product(**data.model_dump())

    try:
        db_session.add(product)
        await db_session.commit()
        await db_session.refresh(product)
    except IntegrityError:
        raise HTTPException(
            status_code=400, detail=f"Category with id {data.category_id} is not exist"
        )

    return {"message": "Product created", "product": product}


async def get(
    id: int,
    db_session: AsyncSession,
):
    """
    Retrieve a product by its unique ID.

    Args:
        id (int): The ID of the product to retrieve.
        db_session (AsyncSession): The asynchronous database session.

    Raises:
        ObjectWithIdNotFound: If no product with the given ID exists.

    Returns:
        Product: The product instance with the specified ID.
    """
    res = await db_session.exec(select(Product).where(Product.id == id))
    product = res.first()

    if product is None:
        raise ObjectWithIdNotFound(id, Product)
    return product


async def get_with_category_slug(category_slug: str, db_session: AsyncSession):
    """
    Retrieve all products associated with a category identified by its slug.

    Args:
        category_slug (str): The slug of the category.
        db_session (AsyncSession): The asynchronous database session.

    Returns:
        List[Product]: A list of products belonging to the specified category.
    """
    category = await categories_service.get_with_slug(category_slug, db_session)
    res = await db_session.exec(
        select(Product).where(Product.category_id == category.id)
    )
    products = res.all()

    return products


async def get_all(db_session: AsyncSession):
    """
    Retrieve all products from the database.

    Args:
        db_session (AsyncSession): The asynchronous database session.

    Returns:
        List[Product]: A list of all product instances.
    """
    res = await db_session.exec(select(Product))
    products = res.all()

    return products


async def update(
    id: int,
    data: UpdateProductSchema,
    db_session: AsyncSession,
):
    """
    Update an existing product's information.

    Args:
        id (int): The ID of the product to update.
        data (UpdateProductSchema): The data to update the product with.
        db_session (AsyncSession): The asynchronous database session.

    Returns:
        dict: A dictionary containing a success message and the updated product instance.
    """
    product = await get(id, db_session)

    for k, v in data.model_dump().items():
        if v is not None:
            setattr(product, k, v)

    db_session.add(product)
    await db_session.commit()
    await db_session.refresh(product)

    return {"message": "Product updated", "product": product}


async def delete(id: int, db_session: AsyncSession):
    """
    Delete a product from the database by its ID.

    Args:
        id (int): The ID of the product to delete.
        db_session (AsyncSession): The asynchronous database session.

    Raises:
        ObjectWithIdNotFound: If no product with the given ID exists.

    Returns:
        None
    """
    product = await get(id, db_session)

    await db_session.delete(product)
    await db_session.commit()
