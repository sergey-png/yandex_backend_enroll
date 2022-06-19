# encoding=utf8

import pytest

API_BASEURL = 'http://localhost:8000'
ROOT_ID = '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1'
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

EXPECTED_TREE = {
    "type": "CATEGORY",
    "name": "Товары",
    "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
    "price": 58599,
    "parentId": None,
    "date": "2022-02-03T15:00:00.000Z",
    "children": [
        {
            "type": "CATEGORY",
            "name": "Телевизоры",
            "id": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
            "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
            "price": 50999,
            "date": "2022-02-03T15:00:00.000Z",
            "children": [
                {
                    "type": "OFFER",
                    "name": "Samson 70\" LED UHD Smart",
                    "id": "98883e8f-0507-482f-bce2-2fb306cf6483",
                    "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                    "price": 32999,
                    "date": "2022-02-03T12:00:00.000Z",
                    "children": None,
                },
                {
                    "type": "OFFER",
                    "name": "Phyllis 50\" LED UHD Smarter",
                    "id": "74b81fda-9cdc-4b63-8927-c978afed5cf4",
                    "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                    "price": 49999,
                    "date": "2022-02-03T12:00:00.000Z",
                    "children": None
                },
                {
                    "type": "OFFER",
                    "name": "Goldstar 65\" LED UHD LOL Very Smart",
                    "id": "73bc3b36-02d1-4245-ab35-3106c9ee1c65",
                    "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                    "price": 69999,
                    "date": "2022-02-03T15:00:00.000Z",
                    "children": None
                }
            ]
        },
        {
            "type": "CATEGORY",
            "name": "Смартфоны",
            "id": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
            "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
            "price": 69999,
            "date": "2022-02-02T12:00:00.000Z",
            "children": [
                {
                    "type": "OFFER",
                    "name": "jPhone 13",
                    "id": "863e1a7a-1304-42ae-943b-179184c077e3",
                    "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
                    "price": 79999,
                    "date": "2022-02-02T12:00:00.000Z",
                    "children": None
                },
                {
                    "type": "OFFER",
                    "name": "Xomiа Readme 10",
                    "id": "b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4",
                    "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
                    "price": 59999,
                    "date": "2022-02-02T12:00:00.000Z",
                    "children": None
                }
            ]
        },
    ]
}

@pytest.mark.asyncio
async def test_import_new_items_1(client):
    global IMPORT_BATCHES
    for index, batch in enumerate(IMPORT_BATCHES):
        response = await client.post(
            '/imports',
            json=batch,
        )
        assert response.status_code == 200, (
            f'Batch import failed on index_{index}, '
            f'response_status_code: {response.status_code} '
            f'expected: 200'
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


@pytest.mark.asyncio
async def test_delete_row_with_id(client):
    response = await client.delete(f'/delete/{ROOT_ID}')
    assert response.status_code == 200
    assert response.json() == {'id': ROOT_ID}


@pytest.mark.asyncio
async def test_import_wrong_format_type(client):
    response = await client.post(
        '/imports',
        json={
            'items': [
                {
                    "type": "OFFERS_Invalid",
                    "name": "Xomiа Readme 10",
                    "id": "b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4",
                    "parentId": None,
                    "price": 59999,
                    "date": "2022-02-02T12:00:00.000Z",
                    "children": None
                }
            ],
            'updateDate': '2022-06-18T10:36:08Z',
        },
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_import_empty_format_name(client):
    response = await client.post(
        '/imports',
        json={
            'items': [
                {
                    "type": "OFFER",
                    "name": "",
                    "id": "b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4",
                    "parentId": None,
                    "price": 59999,
                    "date": "2022-02-02T12:00:00.000Z",
                    "children": None
                }
            ],
            'updateDate': '2022-06-18T10:36:08Z',
        },
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_import_wrong_format_id(client):
    response = await client.post(
        '/imports',
        json={
            'items': [
                {
                    "type": "OFFER",
                    "name": "Xomiа Readme 10",
                    "id": None,
                    "parentId": None,
                    "price": 59999,
                    "date": "2022-02-02T12:00:00.000Z",
                    "children": None
                }
            ],
            'updateDate': '2022-06-18T10:36:08Z',
        },
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_import_wrong_format_parentId(client):
    response = await client.post(
        '/imports',
        json={
            'items': [
                {
                    "type": "OFFER",
                    "name": "Xomiа Readme 10",
                    "id": "b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4",
                    "parentId": "Not exists",
                    "price": 59999,
                    "date": "2022-02-02T12:00:00.000Z",
                    "children": None
                }
            ],
            'updateDate': '2022-06-18T10:36:08Z',
        },
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_import_id_equals_parentId(client):
    response = await client.post(
        '/imports',
        json={
            'items': [
                {
                    "type": "OFFER",
                    "name": "Xomiа Readme 10",
                    "id": "b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4",
                    "parentId": "b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4",
                    "price": 59999,
                    "date": "2022-02-02T12:00:00.000Z",
                    "children": None
                }
            ],
            'updateDate': '2022-06-18T10:36:08Z',
        },
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_import_change_parentId_to_null(client):
    global IMPORT_BATCHES
    for index, batch in enumerate(IMPORT_BATCHES):
        response = await client.post(
            '/imports',
            json=batch,
        )
        assert response.status_code == 200, (
            f'Batch import failed on index_{index}, '
            f'response_status_code: {response.status_code} '
            f'expected: 200'
        )

    response = await client.post(
        '/imports',
        json={
            'items': [
                {
                    "type": "OFFER",
                    "name": "Xomiа Readme 10",
                    "id": "b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4",
                    "parentId": None,
                    "price": 59999,
                    "date": "2022-02-02T12:00:00.000Z",
                    "children": None
                }
            ],
            'updateDate': '2022-06-18T10:36:08Z',
        }
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_import_change_parentId_to_existing(client):
    response = await client.post(
        '/imports',
        json={
            'items': [
                {
                    "type": "OFFER",
                    "name": "Xomiа Readme 10",
                    "id": "b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4",
                    "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                    "price": 59999,
                    "date": "2022-02-02T12:00:00.000Z",
                    "children": None
                }
            ],
            'updateDate': '2022-06-18T10:36:08Z',
        }
    )
    assert response.status_code == 200

    response = await client.post(
        '/imports',
        json={
            'items': [
                {
                    "type": "OFFER",
                    "name": "Xomiа Readme 10",
                    "id": "b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4",
                    "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
                    "price": 59999,
                    "date": "2022-02-02T12:00:00.000Z",
                    "children": None
                }
            ],
            'updateDate': '2022-06-18T10:36:08Z',
        }
    )
    assert response.status_code == 200


# @pytest.mark.asyncio
# async def test_delete_root_category(client):
#     response = await client.delete(f'/delete/{ROOT_ID}')
#     assert response.status_code == 200


@pytest.mark.asyncio
async def test_import_item_offer_with_price_null(client):
    response = await client.post(
        '/imports',
        json={
            'items': [
                {
                    "type": "OFFER",
                    "name": "Xomiа Readme 10",
                    "id": "b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4",
                    "parentId": None,
                    "price": None,
                    "date": "2022-02-02T12:00:00.000Z",
                    "children": None
                }
            ],
            'updateDate': '2022-06-18T10:36:08Z',
        },
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_import_item_offer_with_price_under_zero(client):
    response = await client.post(
        '/imports',
        json={
            'items': [
                {
                    "type": "OFFER",
                    "name": "Xomiа Readme 10",
                    "id": "b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4",
                    "parentId": None,
                    "price": -1,
                    "date": "2022-02-02T12:00:00.000Z",
                    "children": None
                }
            ],
            'updateDate': '2022-06-18T10:36:08Z',
        },
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_import_items_with_same_id(client):
    response = await client.post(
        '/imports',
        json={
            'items': [
                {
                    "type": "OFFER",
                    "name": "Xomiа Readme 10",
                    "id": "b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4",
                    "parentId": None,
                    "price": 59999,
                    "date": "2022-02-02T12:00:00.000Z",
                    "children": None
                },
                {
                    "type": "OFFER",
                    "name": "X Readme 10",
                    "id": "b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4",
                    "parentId": None,
                    "price": 60000,
                    "date": "2022-02-02T12:00:00.000Z",
                    "children": None
                }
            ],
            'updateDate': '2022-06-18T10:36:08Z',
        },
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_import_offer_with_price_for_category(client):
    response = await client.post(
        '/imports',
        json={
            'items': [
                {
                    "type": "CATEGORY",
                    "name": "Xomiа Readme 10",
                    "id": "b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4",
                    "parentId": None,
                    "price": 59999,
                    "date": "2022-02-02T12:00:00.000Z",
                    "children": None
                }
            ],
            'updateDate': '2022-06-18T10:36:08Z',
        },
    )
    assert response.status_code == 400


