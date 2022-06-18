# encoding=utf8

import pytest

API_BASEURL = 'http://localhost:8000'
ROOT_ID = '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1'


@pytest.mark.asyncio
async def test_import_new_items_1(client):
    IMPORT_BATCHES = [
        {
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
        {
            'items': [
                {
                    'type': 'CATEGORY',
                    'name': 'Смартфоны',
                    'id': 'd515e43f-f3f6-4471-bb77-6b455017a2d2',
                    'parentId': '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1',
                },
                {
                    'type': 'OFFER',
                    'name': 'jPhone 13',
                    'id': '863e1a7a-1304-42ae-943b-179184c077e3',
                    'parentId': 'd515e43f-f3f6-4471-bb77-6b455017a2d2',
                    'price': 79999,
                },
                {
                    'type': 'OFFER',
                    'name': 'Xomiа Readme 10',
                    'id': 'b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4',
                    'parentId': 'd515e43f-f3f6-4471-bb77-6b455017a2d2',
                    'price': 59999,
                },
            ],
            'updateDate': '2022-02-02T12:00:00.000Z',
        },
        {
            'items': [
                {
                    'type': 'CATEGORY',
                    'name': 'Телевизоры',
                    'id': '1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2',
                    'parentId': '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1',
                },
                {
                    'type': 'OFFER',
                    'name': "Samson 70\" LED UHD Smart",
                    'id': '98883e8f-0507-482f-bce2-2fb306cf6483',
                    'parentId': '1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2',
                    'price': 32999,
                },
                {
                    'type': 'OFFER',
                    'name': "Phyllis 50\" LED UHD Smarter",
                    'id': '74b81fda-9cdc-4b63-8927-c978afed5cf4',
                    'parentId': '1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2',
                    'price': 49999,
                },
            ],
            'updateDate': '2022-02-03T12:00:00.000Z',
        },
        {
            'items': [
                {
                    'type': 'OFFER',
                    'name': "Goldstar 65\" LED UHD LOL Very Smart",
                    'id': '73bc3b36-02d1-4245-ab35-3106c9ee1c65',
                    'parentId': '1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2',
                    'price': 69999,
                }
            ],
            'updateDate': '2022-02-03T15:00:00.000Z',
        },
    ]
    for index, batch in enumerate(IMPORT_BATCHES):
        response = await client.post(
            '/imports',
            json=batch,
        )
        assert response.status_code == 200, (
            f'Batch import failed with #{index}, '
            f'response_status_code: {response.status_code}'
        )


@pytest.mark.asyncio
async def test_imports_post_validation_error(client):
    response = await client.post('/imports')
    assert (
        response.status_code == 400
    ), f'Response status code is {response.status_code}, expected 400'


@pytest.mark.asyncio
async def test_wrong_import_iso_date_format_1(client):
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
            'updateDate': '2022-??-01T12:00:00.000Z',
        },
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_wrong_import_iso_date_format_1(client):
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
            'updateDate': '20220618T103608Z',
        },
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_wright_import_iso_date_format_1(client):
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
            'updateDate': '1980-12-01T00:00:32.000Z',
        },
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_wright_import_iso_date_format_2(client):
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
            'updateDate': '2022-06-18T10:36:08Z',
        },
    )
    assert response.status_code == 200
