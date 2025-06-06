from sqlmodel.ext.asyncio.session import AsyncSession

from fastapi import HTTPException

from users import service as users_service

from .utils import verify_password
from .schemas import LoginSchema


async def auth_user(credentials: LoginSchema, db_session: AsyncSession):
    """
    Authenticate a user by their phone number and password.

    Args:
        credentials (LoginSchema): The login credentials containing phone number and password.
        db_session (AsyncSession): The asynchronous database session.

    Raises:
        HTTPException: 
            - 403 if the credentials are invalid (wrong phone number or password).

    Returns:
        User: The authenticated user instance.
    """
    user = await users_service.get_with_phone_number(
        credentials.phone_number, db_session
    )
    if user:
        if verify_password(credentials.password, user.hashed_password):
            return user
    raise HTTPException(status_code=403, detail="Invalid credentials")
