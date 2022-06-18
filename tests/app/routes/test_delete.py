# encoding=utf8


import pytest
import logging

API_BASEURL = 'http://localhost:8000'
ROOT_ID = '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1'


@pytest.mark.asyncio
async def test_delete_row_with_id(client):
    response = await client.delete(f'/delete/{ROOT_ID}')
    assert response.status_code == 200
    assert response.json() == {'id': ROOT_ID}
