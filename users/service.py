from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from sqlalchemy.exc import IntegrityError

from fastapi import HTTPException

from typing import Union

import re

from auth.utils import hash_password

from http_exceptions import ObjectWithIdNotFound

from config import settings

from .models import User
from .schemas import CreateUserSchema, CreateAdminSchema, UpdateUserSchema


async def create(
    data: Union[CreateUserSchema, CreateAdminSchema], db_session: AsyncSession
):
    """
    Create a new user or admin in the database.

    Args:
        data (Union[CreateUserSchema, CreateAdminSchema]): The user data to create.
            If `CreateAdminSchema` is provided, a secret must be validated to assign admin role.
        db_session (AsyncSession): The asynchronous database session.

    Raises:
        HTTPException:
            - 403 if admin secret is invalid.
            - 409 if a user with the same phone number already exists.

    Returns:
        dict: A dictionary containing a success message and the created user instance.
    """
    user = User(**data.model_dump())
    user.hashed_password = hash_password(data.password)

    try:
        if data.secret != settings.ADMIN_SECRET:
            raise HTTPException(status_code=403, detail="Invalid secret")
        user.role = "admin"
    except AttributeError:
        pass

    try:
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)
    except IntegrityError:
        raise HTTPException(
            status_code=409, detail="User with this phone number already exists"
        )

    return {"message": "User created", "user": user}


async def get(
    id: int,
    db_session: AsyncSession,
):
    """
    Retrieve a user by their unique ID.

    Args:
        id (int): The ID of the user to retrieve.
        db_session (AsyncSession): The asynchronous database session.

    Raises:
        ObjectWithIdNotFound: If no user with the given ID exists.

    Returns:
        User: The user instance with the specified ID.
    """
    res = await db_session.exec(select(User).where(User.id == id))
    user = res.first()

    if not user:
        raise ObjectWithIdNotFound(id, User)
    return user


async def get_with_phone_number(phone_number: str, db_session: AsyncSession):
    """
    Retrieve a user by their phone number.

    Args:
        phone_number (str): The phone number of the user to retrieve. Must match E.164 format.
        db_session (AsyncSession): The asynchronous database session.

    Raises:
        HTTPException:
            - 400 if the phone number format is invalid.
            - 404 if no user with the given phone number is found.

    Returns:
        User: The user instance with the specified phone number.
    """
    if not re.fullmatch(r"^\+[1-9]\d{1,14}$", phone_number):
        raise HTTPException(status_code=400, detail="Invalid phone number format")
    res = await db_session.exec(select(User).where(User.phone_number == phone_number))
    user = res.first()

    if not user:
        raise HTTPException(
            status_code=404, detail=f"User with phone number '{phone_number}' not found"
        )
    return user


async def get_all(db_session: AsyncSession):
    """
    Retrieve all users from the database.

    Args:
        db_session (AsyncSession): The asynchronous database session.

    Returns:
        List[User]: A list of all user instances.
    """
    res = await db_session.exec(select(User))
    users = res.all()

    return users


async def update(
    id: int,
    data: UpdateUserSchema,
    db_session: AsyncSession,
):
    """
    Update an existing user's information.

    Args:
        id (int): The ID of the user to update.
        data (UpdateUserSchema): The data to update the user with. Password will be hashed if provided.
        db_session (AsyncSession): The asynchronous database session.

    Returns:
        dict: A dictionary containing a success message and the updated user instance.
    """
    user = await get(id, db_session)

    print(data.model_dump().items())
    for k, v in data.model_dump().items():
        if v is not None:
            if k != "password":
                setattr(user, k, v)
    if data.password:
        user.hashed_password = hash_password(data.password)

    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    return {"message": "User updated", "user": user}


async def delete(
    id: int,
    db_session: AsyncSession,
):
    """
    Delete a user from the database by their ID.

    Args:
        id (int): The ID of the user to delete.
        db_session (AsyncSession): The asynchronous database session.

    Raises:
        ObjectWithIdNotFound: If no user with the given ID exists.

    Returns:
        None
    """
    user = await get(id, db_session)

    await db_session.delete(user)
    await db_session.commit()
