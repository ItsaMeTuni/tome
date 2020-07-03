import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


async def test_index(client: AsyncClient):
    response = await client.get("/")
    assert response.status_code == 404


async def test_api(client: AsyncClient):
    response = await client.get("/api/")
    assert response.status_code == 200
    assert response.json() == "hello, world!"
