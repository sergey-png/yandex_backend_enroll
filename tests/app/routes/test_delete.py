# encoding=utf8


import pytest

API_BASEURL = 'http://localhost:8000'
ROOT_ID = '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1'


@pytest.mark.asyncio
async def test_delete_non_used_id(client):
    response = await client.delete(f'/delete/0347sgda-5436-34gh-dsaf-845hjgdgfhg1')
    assert response.status_code == 404
    assert response.json() == {'detail': 'Item not found'}

