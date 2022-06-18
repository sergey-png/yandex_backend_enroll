import pytest
from httpx import AsyncClient

from app.__main__ import app


@pytest.fixture()
async def client():
    async with AsyncClient(app=app, base_url='http://localhost:8000/') as client:
        yield client
