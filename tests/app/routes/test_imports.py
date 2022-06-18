# encoding=utf8

import pytest

API_BASEURL = 'http://localhost:8000'
ROOT_ID = '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1'


@pytest.mark.asyncio
async def test_imports_post_validation_error(client):
    response = await client.post('/imports')
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_imports_post_validation_with_data_without_parentid(client):
    response = await client.post(
        '/imports',
        json={
            'items': [
                {
                    'type': 'CATEGORY',
                    'name': 'Товары',
                    'id': '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1',
                    'parentId': None,
                }
            ],
            'updateDate': '2022-02-01T12:00:00.000Z',
        },
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_import_iso_date_format(client):
    response = await client.post(
        '/imports',
        json={
            'items': [
                {
                    'type': 'CATEGORY',
                    'name': 'Товары',
                    'id': '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1',
                    'parentId': None,
                }
            ],
            'updateDate': '2022-22-01T12:00:00.000Z',
        },
    )
    assert response.status_code == 400
