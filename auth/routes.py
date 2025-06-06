from sqlmodel.ext.asyncio.session import AsyncSession

from fastapi import APIRouter, Depends

from typing import Annotated, Dict, Union

import time

from database import get_db_session

from config import settings

from .service import auth_user
from .schemas import LoginSchema
from .utils import create_access_token


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/token", response_model=Dict[str, Union[str, int]])
async def get_access_token(
    credentials: LoginSchema,
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
):
    user = await auth_user(credentials, db_session)

    return {
        "access_token": create_access_token(user),
        "expires_at": int(time.time() + settings.ACCESS_TOKEN_EXPIRATION_TIME * 60),
    }
