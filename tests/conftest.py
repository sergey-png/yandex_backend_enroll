import pytest
import pytest_asyncio
from httpx import AsyncClient

from app.__main__ import app

API_BASEURL = 'http://localhost:8000'


@pytest_asyncio.fixture
@pytest.mark.asyncio
async def client():
    async with AsyncClient(
        app=app, base_url=API_BASEURL
    ) as client:
        yield client
