from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from typing import AsyncGenerator

from sqlmodel.ext.asyncio.session import AsyncSession

from config import settings

engine = create_async_engine(settings.POSTGRES_URL)

session_maker = sessionmaker(bind=engine, class_=AsyncSession)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with session_maker() as session:
        try:
            yield session
        finally:
            await session.close()
