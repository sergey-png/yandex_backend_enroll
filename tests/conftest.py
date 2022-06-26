import pytest
import pytest_asyncio
from httpx import AsyncClient

from app.__main__ import app


@pytest_asyncio.fixture
@pytest.mark.asyncio
async def client():
    async with AsyncClient(
        app=app, base_url='http://0.0.0.0:80/'
    ) as client:
        yield client
