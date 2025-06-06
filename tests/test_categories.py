import pytest
import pytest_asyncio

from unittest.mock import call, create_autospec, MagicMock, AsyncMock

from httpx import AsyncClient, ASGITransport

from sqlmodel.ext.asyncio.session import AsyncSession

from app import app

from database import get_db_session

from auth import admin

from categories import Category
from categories.schemas import CreateCategorySchema, UpdateCategorySchema

from .client import client

test_category_data = CreateCategorySchema(title="Drinks", slug="drinks")


async def dummy_dependency():
    return


async def get_mock_db_session():
    async with mock_sessionmaker() as session:
        yield session


app.dependency_overrides[admin] = dummy_dependency
app.dependency_overrides[get_db_session] = get_mock_db_session


@pytest_asyncio.fixture(scope="session")
async def client():
    yield AsyncClient(transport=ASGITransport(app=app), base_url="http://test")


@pytest.mark.asyncio
async def test_create_category(client):
    response = await client.post("/categories", json=test_category_data.model_dump())

    assert response.status_code == 201


@pytest.mark.asyncio
async def test_get_category_or_categories(client):
    id_response = await client.get("/categories?id=1")
    slug_response = await client.get(f"/categories?slug={test_category_data.slug}")
    all_response = await client.get("/categories")

    assert id_response.status_code == 200
    assert slug_response.status_code == 200
    assert all_response.status_code == 200

    assert isinstance(all_response.json(), list)
