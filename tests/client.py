import pytest_asyncio

from httpx import AsyncClient, ASGITransport


@pytest_asyncio.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app)) as client:
        yield client
