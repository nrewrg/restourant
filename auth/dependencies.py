from typing import Annotated, TYPE_CHECKING

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer

from sqlalchemy.ext.asyncio.session import AsyncSession

from database import get_db_session

from users import service as users_service

from http_exceptions import AccessDenied

from .utils import decode_token

if TYPE_CHECKING:
    from users import User

access_token_bearer = HTTPBearer(description="Access token bearer")


async def get_current_user(
    bearer: Annotated[str, Depends(access_token_bearer)],
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
):
    token_data: dict = decode_token(token=bearer.credentials)
    return await users_service.get(id=int(token_data["sub"]), db_session=db_session)


async def admin(
    current_user: Annotated["User", Depends(get_current_user)],
):
    if current_user.role != "admin":
        raise AccessDenied()
    return current_user
