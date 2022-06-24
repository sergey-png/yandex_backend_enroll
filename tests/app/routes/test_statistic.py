# encoding=utf8
import logging

import pytest

logging.getLogger(__name__)

API_BASEURL = 'http://localhost:8000'
ROOT_ID = '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1'


@pytest.mark.asyncio
async def test_get_statistic_1(client):
    item_id = '73bc3b36-02d1-4245-ab35-3106c9ee1c65'
    response = await client.get(
        f'node/{item_id}/statistic?dateStart=2022-02-01T00%3A00%3A00.000Z'
        f'&dateEnd=2022-02-04T00%3A00%3A00.000Z'
    )

    EXPECTED_TREE_2 = {
        'items': [
            {
                'id': '73bc3b36-02d1-4245-ab35-3106c9ee1c65',
                'name': "Goldstar 65\" LED UHD LOL Very Smart",
                'parentId': '1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2',
                'type': 'OFFER',
                'price': 1000000,
                'date': '2022-02-03T12:00:00.000Z',
            },
            {
                'id': '73bc3b36-02d1-4245-ab35-3106c9ee1c65',
                'name': "Goldstar 65\" LED UHD LOL Very Smart",
                'parentId': '1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2',
                'type': 'OFFER',
                'price': 69999,
                'date': '2022-02-03T15:00:00.000Z',
            },
        ]
    }

    assert response.status_code == 200
    assert response.json() == EXPECTED_TREE_2


@pytest.mark.asyncio
async def test_get_statistic_2(client):
    item_id = '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1'
    response = await client.get(
        f'node/{item_id}/statistic?dateStart=2022-02-01T00%3A00%3A00.000Z'
        f'&dateEnd=2022-02-04T00%3A00%3A00.000Z'
    )

    EXPECTED_TREE_2 = {
        'items': [
            {
                'id': '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1',
                'name': 'Товары',
                'parentId': None,
                'type': 'CATEGORY',
                'price': None,
                'date': '2022-02-01T12:00:00.000Z',
            },
            {
                'id': '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1',
                'name': 'Товары',
                'parentId': None,
                'type': 'CATEGORY',
                'price': 69999,
                'date': '2022-02-02T12:00:00.000Z',
            },
            {
                'id': '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1',
                'name': 'Товары',
                'parentId': None,
                'type': 'CATEGORY',
                'price': 244599,
                'date': '2022-02-03T12:00:00.000Z',
            },
            {
                'id': '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1',
                'name': 'Товары',
                'parentId': None,
                'type': 'CATEGORY',
                'price': 58599,
                'date': '2022-02-03T15:00:00.000Z',
            },
        ]
    }

    assert response.status_code == 200
    assert response.json() == EXPECTED_TREE_2


@pytest.mark.asyncio
async def test_get_statistic_with_non_existing_id_1(client):
    item_id = 'Not_exists'
    response = await client.get(
        f'node/{item_id}/statistic?dateStart=2022-02-01T00%3A00%3A00.000Z'
        f'&dateEnd=2022-02-04T00%3A00%3A00.000Z'
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_statistic_with_wrong_dataStart(client):
    item_id = '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1'
    response = await client.get(
        f'node/{item_id}/statistic?dateStart=2022-??-01T00%3A00%3A00.000Z'
        f'&dateEnd=2022-02-04T00%3A00%3A00.000Z'
    )

    assert response.status_code == 400


@pytest.mark.asyncio
async def test_get_statistic_with_wrong_dataEnd(client):
    item_id = '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1'
    response = await client.get(
        f'node/{item_id}/statistic?dateStart=2022-02-01T00%3A00%3A00.000Z'
        f'&dateEnd=2022-??-04T00%3A00%3A00.000Z'
    )

    assert response.status_code == 400


@pytest.mark.asyncio
async def test_delete_all(client):
    response = await client.delete(
        '/delete/069cb8d7-bbdd-47d3-ad8f-82ef4c269df1'
    )
    assert response.status_code == 200
