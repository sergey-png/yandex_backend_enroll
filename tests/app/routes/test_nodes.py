# encoding=utf8
import json
import logging
import subprocess

import pytest

logging.getLogger('uvicorn.error')

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
    'type': 'CATEGORY',
    'name': 'Товары',
    'id': '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1',
    'price': 58599,
    'parentId': None,
    'date': '2022-02-03T15:00:00.000Z',
    'children': [
        {
            'type': 'CATEGORY',
            'name': 'Телевизоры',
            'id': '1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2',
            'parentId': '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1',
            'price': 50999,
            'date': '2022-02-03T15:00:00.000Z',
            'children': [
                {
                    'type': 'OFFER',
                    'name': "Samson 70\" LED UHD Smart",
                    'id': '98883e8f-0507-482f-bce2-2fb306cf6483',
                    'parentId': '1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2',
                    'price': 32999,
                    'date': '2022-02-03T12:00:00.000Z',
                    'children': None,
                },
                {
                    'type': 'OFFER',
                    'name': "Phyllis 50\" LED UHD Smarter",
                    'id': '74b81fda-9cdc-4b63-8927-c978afed5cf4',
                    'parentId': '1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2',
                    'price': 49999,
                    'date': '2022-02-03T12:00:00.000Z',
                    'children': None,
                },
                {
                    'type': 'OFFER',
                    'name': "Goldstar 65\" LED UHD LOL Very Smart",
                    'id': '73bc3b36-02d1-4245-ab35-3106c9ee1c65',
                    'parentId': '1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2',
                    'price': 69999,
                    'date': '2022-02-03T15:00:00.000Z',
                    'children': None,
                },
            ],
        },
        {
            'type': 'CATEGORY',
            'name': 'Смартфоны',
            'id': 'd515e43f-f3f6-4471-bb77-6b455017a2d2',
            'parentId': '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1',
            'price': 69999,
            'date': '2022-02-02T12:00:00.000Z',
            'children': [
                {
                    'type': 'OFFER',
                    'name': 'jPhone 13',
                    'id': '863e1a7a-1304-42ae-943b-179184c077e3',
                    'parentId': 'd515e43f-f3f6-4471-bb77-6b455017a2d2',
                    'price': 79999,
                    'date': '2022-02-02T12:00:00.000Z',
                    'children': None,
                },
                {
                    'type': 'OFFER',
                    'name': 'Xomiа Readme 10',
                    'id': 'b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4',
                    'parentId': 'd515e43f-f3f6-4471-bb77-6b455017a2d2',
                    'price': 59999,
                    'date': '2022-02-02T12:00:00.000Z',
                    'children': None,
                },
            ],
        },
    ],
}


@pytest.mark.asyncio
async def test_delete_row_with_id(client):
    response = await client.delete(f'/delete/{ROOT_ID}')
    assert response.status_code == 200
    assert response.json() == {'id': ROOT_ID}


@pytest.mark.asyncio
async def test_restore_all_items(client):
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
async def test_get_existing_tree_with_id_1(client):

    response = await client.get(f'/nodes/{ROOT_ID}')

    assert response.status_code == 200
    response_json = response.json()
    logging.info('RESPONSE BEFORE: %s', response_json)
    deep_sort_children(response_json)
    logging.info('RESPONSE AFTER: %s', response_json)

    deep_sort_children(EXPECTED_TREE)
    print_diff(EXPECTED_TREE, response_json)
    assert (
        response_json == EXPECTED_TREE
    ), "Response tree doesn't match expected tree"


def deep_sort_children(node):
    if node.get('children'):
        node['children'].sort(key=lambda x: x['id'])

        for child in node['children']:
            deep_sort_children(child)


def print_diff(expected, response):
    with open('expected.json', 'w') as f:
        json.dump(expected, f, indent=2, ensure_ascii=False, sort_keys=True)
        f.write('\n')

    with open('response.json', 'w') as f:
        json.dump(response, f, indent=2, ensure_ascii=False, sort_keys=True)
        f.write('\n')

    subprocess.run(
        [
            'git',
            '--no-pager',
            'diff',
            '--no-index',
            'expected.json',
            'response.json',
        ]
    )


@pytest.mark.asyncio
async def test_get_non_existing_tree_with_id(client):
    response = await client.get(f'/nodes/NON_EXISTING_ID')
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_import_offer_to_update_itself(client):
    response = await client.post(
        '/imports',
        json={
            'items': [
                {
                    'type': 'OFFER',
                    'name': 'Update Readme 10',
                    'id': '73bc3b36-02d1-4245-ab35-3106c9ee1c65',
                    'parentId': '1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2',
                    'price': 30000,
                    'date': '2022-02-02T16:00:00.000Z',
                    'children': None,
                }
            ],
            'updateDate': '2022-06-18T17:36:08Z',
        },
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_existing_tree_with_id_2(client):

    response = await client.get(f'/nodes/{ROOT_ID}')

    assert response.status_code == 200
    response_json = response.json()
    logging.info('RESPONSE BEFORE: %s', response_json)
    deep_sort_children(response_json)
    logging.info('RESPONSE AFTER: %s', response_json)

    EXPECTED_TREE_2 = {
        'type': 'CATEGORY',
        'name': 'Товары',
        'id': '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1',
        'price': 50599,
        'parentId': None,
        'date': '2022-06-18T17:36:08.000Z',
        'children': [
            {
                'type': 'CATEGORY',
                'name': 'Телевизоры',
                'id': '1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2',
                'parentId': '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1',
                'price': 37666,
                'date': '2022-06-18T17:36:08.000Z',
                'children': [
                    {
                        'type': 'OFFER',
                        'name': "Samson 70\" LED UHD Smart",
                        'id': '98883e8f-0507-482f-bce2-2fb306cf6483',
                        'parentId': '1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2',
                        'price': 32999,
                        'date': '2022-02-03T12:00:00.000Z',
                        'children': None,
                    },
                    {
                        'type': 'OFFER',
                        'name': "Phyllis 50\" LED UHD Smarter",
                        'id': '74b81fda-9cdc-4b63-8927-c978afed5cf4',
                        'parentId': '1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2',
                        'price': 49999,
                        'date': '2022-02-03T12:00:00.000Z',
                        'children': None,
                    },
                    {
                        'type': 'OFFER',
                        'name': 'Update Readme 10',
                        'id': '73bc3b36-02d1-4245-ab35-3106c9ee1c65',
                        'parentId': '1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2',
                        'price': 30000,
                        'date': '2022-06-18T17:36:08.000Z',
                        'children': None,
                    },
                ],
            },
            {
                'type': 'CATEGORY',
                'name': 'Смартфоны',
                'id': 'd515e43f-f3f6-4471-bb77-6b455017a2d2',
                'parentId': '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1',
                'price': 69999,
                'date': '2022-02-02T12:00:00.000Z',
                'children': [
                    {
                        'type': 'OFFER',
                        'name': 'jPhone 13',
                        'id': '863e1a7a-1304-42ae-943b-179184c077e3',
                        'parentId': 'd515e43f-f3f6-4471-bb77-6b455017a2d2',
                        'price': 79999,
                        'date': '2022-02-02T12:00:00.000Z',
                        'children': None,
                    },
                    {
                        'type': 'OFFER',
                        'name': 'Xomiа Readme 10',
                        'id': 'b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4',
                        'parentId': 'd515e43f-f3f6-4471-bb77-6b455017a2d2',
                        'price': 59999,
                        'date': '2022-02-02T12:00:00.000Z',
                        'children': None,
                    },
                ],
            },
        ],
    }

    deep_sort_children(EXPECTED_TREE_2)
    print_diff(EXPECTED_TREE_2, response_json)
    assert (
        response_json == EXPECTED_TREE_2
    ), "Response tree doesn't match expected tree"


@pytest.mark.asyncio
async def test_import_category_to_update_itself(client):
    response = await client.post(
        '/imports',
        json={
            'items': [
                {
                    'type': 'CATEGORY',
                    'name': 'Телекомуникации',
                    'id': '1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2',
                    'parentId': '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1',
                }
            ],
            'updateDate': '2023-01-01T10:00:00Z',
        },
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_existing_tree_with_id_3(client):

    response = await client.get(f'/nodes/{ROOT_ID}')

    assert response.status_code == 200
    response_json = response.json()
    logging.info('RESPONSE BEFORE: %s', response_json)
    deep_sort_children(response_json)
    logging.info('RESPONSE AFTER: %s', response_json)

    EXPECTED_TREE_2 = {
        'type': 'CATEGORY',
        'name': 'Товары',
        'id': '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1',
        'price': 50599,
        'parentId': None,
        'date': '2023-01-01T10:00:00.000Z',
        'children': [
            {
                'type': 'CATEGORY',
                'name': 'Телекомуникации',
                'id': '1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2',
                'parentId': '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1',
                'price': 37666,
                'date': '2023-01-01T10:00:00.000Z',
                'children': [
                    {
                        'type': 'OFFER',
                        'name': "Samson 70\" LED UHD Smart",
                        'id': '98883e8f-0507-482f-bce2-2fb306cf6483',
                        'parentId': '1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2',
                        'price': 32999,
                        'date': '2022-02-03T12:00:00.000Z',
                        'children': None,
                    },
                    {
                        'type': 'OFFER',
                        'name': "Phyllis 50\" LED UHD Smarter",
                        'id': '74b81fda-9cdc-4b63-8927-c978afed5cf4',
                        'parentId': '1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2',
                        'price': 49999,
                        'date': '2022-02-03T12:00:00.000Z',
                        'children': None,
                    },
                    {
                        'type': 'OFFER',
                        'name': 'Update Readme 10',
                        'id': '73bc3b36-02d1-4245-ab35-3106c9ee1c65',
                        'parentId': '1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2',
                        'price': 30000,
                        'date': '2022-06-18T17:36:08.000Z',
                        'children': None,
                    },
                ],
            },
            {
                'type': 'CATEGORY',
                'name': 'Смартфоны',
                'id': 'd515e43f-f3f6-4471-bb77-6b455017a2d2',
                'parentId': '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1',
                'price': 69999,
                'date': '2022-02-02T12:00:00.000Z',
                'children': [
                    {
                        'type': 'OFFER',
                        'name': 'jPhone 13',
                        'id': '863e1a7a-1304-42ae-943b-179184c077e3',
                        'parentId': 'd515e43f-f3f6-4471-bb77-6b455017a2d2',
                        'price': 79999,
                        'date': '2022-02-02T12:00:00.000Z',
                        'children': None,
                    },
                    {
                        'type': 'OFFER',
                        'name': 'Xomiа Readme 10',
                        'id': 'b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4',
                        'parentId': 'd515e43f-f3f6-4471-bb77-6b455017a2d2',
                        'price': 59999,
                        'date': '2022-02-02T12:00:00.000Z',
                        'children': None,
                    },
                ],
            },
        ],
    }

    deep_sort_children(EXPECTED_TREE_2)
    print_diff(EXPECTED_TREE_2, response_json)
    assert (
        response_json == EXPECTED_TREE_2
    ), "Response tree doesn't match expected tree"


@pytest.mark.asyncio
async def test_change_offer_parentId_to_none(client):
    response = await client.post(
        '/imports',
        json={
            'items': [
                {
                    'type': 'OFFER',
                    'name': 'Phyllis 50" LED UHD Smarter',
                    'id': '74b81fda-9cdc-4b63-8927-c978afed5cf4',
                    'parentId': None,
                    'price': 50000,
                }
            ],
            'updateDate': '2024-01-01T10:00:00Z',
        },
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_existing_tree_with_id_4(client):

    response = await client.get(f'/nodes/{ROOT_ID}')

    assert response.status_code == 200
    response_json = response.json()
    logging.info('RESPONSE BEFORE: %s', response_json)
    deep_sort_children(response_json)
    logging.info('RESPONSE AFTER: %s', response_json)

    EXPECTED_TREE_2 = {
        'type': 'CATEGORY',
        'name': 'Товары',
        'id': '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1',
        'price': 50749,
        'parentId': None,
        'date': '2024-01-01T10:00:00.000Z',
        'children': [
            {
                'type': 'CATEGORY',
                'name': 'Телекомуникации',
                'id': '1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2',
                'parentId': '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1',
                'price': 31499,
                'date': '2024-01-01T10:00:00.000Z',
                'children': [
                    {
                        'type': 'OFFER',
                        'name': "Samson 70\" LED UHD Smart",
                        'id': '98883e8f-0507-482f-bce2-2fb306cf6483',
                        'parentId': '1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2',
                        'price': 32999,
                        'date': '2022-02-03T12:00:00.000Z',
                        'children': None,
                    },
                    {
                        'type': 'OFFER',
                        'name': 'Update Readme 10',
                        'id': '73bc3b36-02d1-4245-ab35-3106c9ee1c65',
                        'parentId': '1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2',
                        'price': 30000,
                        'date': '2022-06-18T17:36:08.000Z',
                        'children': None,
                    },
                ],
            },
            {
                'type': 'CATEGORY',
                'name': 'Смартфоны',
                'id': 'd515e43f-f3f6-4471-bb77-6b455017a2d2',
                'parentId': '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1',
                'price': 69999,
                'date': '2022-02-02T12:00:00.000Z',
                'children': [
                    {
                        'type': 'OFFER',
                        'name': 'jPhone 13',
                        'id': '863e1a7a-1304-42ae-943b-179184c077e3',
                        'parentId': 'd515e43f-f3f6-4471-bb77-6b455017a2d2',
                        'price': 79999,
                        'date': '2022-02-02T12:00:00.000Z',
                        'children': None,
                    },
                    {
                        'type': 'OFFER',
                        'name': 'Xomiа Readme 10',
                        'id': 'b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4',
                        'parentId': 'd515e43f-f3f6-4471-bb77-6b455017a2d2',
                        'price': 59999,
                        'date': '2022-02-02T12:00:00.000Z',
                        'children': None,
                    },
                ],
            },
        ],
    }

    deep_sort_children(EXPECTED_TREE_2)
    print_diff(EXPECTED_TREE_2, response_json)
    assert (
        response_json == EXPECTED_TREE_2
    ), "Response tree doesn't match expected tree"


@pytest.mark.asyncio
async def test_change_category_parentId_to_none(client):
    response = await client.post(
        '/imports',
        json={
            'items': [
                {
                    'type': 'CATEGORY',
                    'name': 'Телевизоры Back',
                    'id': '1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2',
                    'parentId': None,
                }
            ],
            'updateDate': '2025-01-01T10:00:00Z',
        },
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_existing_tree_with_id_5(client):

    response = await client.get(f'/nodes/{ROOT_ID}')

    assert response.status_code == 200
    response_json = response.json()
    logging.info('RESPONSE BEFORE: %s', response_json)
    deep_sort_children(response_json)
    logging.info('RESPONSE AFTER: %s', response_json)

    EXPECTED_TREE_2 = {
        'type': 'CATEGORY',
        'name': 'Товары',
        'id': '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1',
        'price': 69999,
        'parentId': None,
        'date': '2025-01-01T10:00:00.000Z',
        'children': [
            {
                'type': 'CATEGORY',
                'name': 'Смартфоны',
                'id': 'd515e43f-f3f6-4471-bb77-6b455017a2d2',
                'parentId': '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1',
                'price': 69999,
                'date': '2022-02-02T12:00:00.000Z',
                'children': [
                    {
                        'type': 'OFFER',
                        'name': 'jPhone 13',
                        'id': '863e1a7a-1304-42ae-943b-179184c077e3',
                        'parentId': 'd515e43f-f3f6-4471-bb77-6b455017a2d2',
                        'price': 79999,
                        'date': '2022-02-02T12:00:00.000Z',
                        'children': None,
                    },
                    {
                        'type': 'OFFER',
                        'name': 'Xomiа Readme 10',
                        'id': 'b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4',
                        'parentId': 'd515e43f-f3f6-4471-bb77-6b455017a2d2',
                        'price': 59999,
                        'date': '2022-02-02T12:00:00.000Z',
                        'children': None,
                    },
                ],
            },
        ],
    }

    deep_sort_children(EXPECTED_TREE_2)
    print_diff(EXPECTED_TREE_2, response_json)
    assert (
        response_json == EXPECTED_TREE_2
    ), "Response tree doesn't match expected tree"


@pytest.mark.asyncio
async def test_get_existing_tree_with_id_6(client):

    response = await client.get(f'/nodes/1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2')

    assert response.status_code == 200
    response_json = response.json()
    logging.info('RESPONSE BEFORE: %s', response_json)
    deep_sort_children(response_json)
    logging.info('RESPONSE AFTER: %s', response_json)

    EXPECTED_TREE_2 = {
        'type': 'CATEGORY',
        'name': 'Телевизоры Back',
        'id': '1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2',
        'parentId': None,
        'price': 31499,
        'date': '2025-01-01T10:00:00.000Z',
        'children': [
            {
                'type': 'OFFER',
                'name': "Samson 70\" LED UHD Smart",
                'id': '98883e8f-0507-482f-bce2-2fb306cf6483',
                'parentId': '1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2',
                'price': 32999,
                'date': '2022-02-03T12:00:00.000Z',
                'children': None,
            },
            {
                'type': 'OFFER',
                'name': 'Update Readme 10',
                'id': '73bc3b36-02d1-4245-ab35-3106c9ee1c65',
                'parentId': '1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2',
                'price': 30000,
                'date': '2022-06-18T17:36:08.000Z',
                'children': None,
            },
        ],
    }

    deep_sort_children(EXPECTED_TREE_2)
    print_diff(EXPECTED_TREE_2, response_json)
    assert (
        response_json == EXPECTED_TREE_2
    ), "Response tree doesn't match expected tree"


@pytest.mark.asyncio
async def test_change_category_parentId_from_none_to_existing(client):
    response = await client.post(
        '/imports',
        json={
            'items': [
                {
                    'type': 'CATEGORY',
                    'name': 'Телевизоры',
                    'id': '1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2',
                    'parentId': '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1',
                }
            ],
            'updateDate': '2026-01-01T10:00:00Z',
        },
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_existing_tree_with_id_7(client):

    response = await client.get(f'/nodes/{ROOT_ID}')

    assert response.status_code == 200
    response_json = response.json()
    logging.info('RESPONSE BEFORE: %s', response_json)
    deep_sort_children(response_json)
    logging.info('RESPONSE AFTER: %s', response_json)

    EXPECTED_TREE_2 = {
        'type': 'CATEGORY',
        'name': 'Товары',
        'id': '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1',
        'price': 50749,
        'parentId': None,
        'date': '2026-01-01T10:00:00.000Z',
        'children': [
            {
                'type': 'CATEGORY',
                'name': 'Телевизоры',
                'id': '1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2',
                'parentId': '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1',
                'price': 31499,
                'date': '2026-01-01T10:00:00.000Z',
                'children': [
                    {
                        'type': 'OFFER',
                        'name': "Samson 70\" LED UHD Smart",
                        'id': '98883e8f-0507-482f-bce2-2fb306cf6483',
                        'parentId': '1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2',
                        'price': 32999,
                        'date': '2022-02-03T12:00:00.000Z',
                        'children': None,
                    },
                    {
                        'type': 'OFFER',
                        'name': 'Update Readme 10',
                        'id': '73bc3b36-02d1-4245-ab35-3106c9ee1c65',
                        'parentId': '1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2',
                        'price': 30000,
                        'date': '2022-06-18T17:36:08.000Z',
                        'children': None,
                    },
                ],
            },
            {
                'type': 'CATEGORY',
                'name': 'Смартфоны',
                'id': 'd515e43f-f3f6-4471-bb77-6b455017a2d2',
                'parentId': '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1',
                'price': 69999,
                'date': '2022-02-02T12:00:00.000Z',
                'children': [
                    {
                        'type': 'OFFER',
                        'name': 'jPhone 13',
                        'id': '863e1a7a-1304-42ae-943b-179184c077e3',
                        'parentId': 'd515e43f-f3f6-4471-bb77-6b455017a2d2',
                        'price': 79999,
                        'date': '2022-02-02T12:00:00.000Z',
                        'children': None,
                    },
                    {
                        'type': 'OFFER',
                        'name': 'Xomiа Readme 10',
                        'id': 'b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4',
                        'parentId': 'd515e43f-f3f6-4471-bb77-6b455017a2d2',
                        'price': 59999,
                        'date': '2022-02-02T12:00:00.000Z',
                        'children': None,
                    },
                ],
            },
        ],
    }

    deep_sort_children(EXPECTED_TREE_2)
    print_diff(EXPECTED_TREE_2, response_json)
    assert (
        response_json == EXPECTED_TREE_2
    ), "Response tree doesn't match expected tree"


@pytest.mark.asyncio
async def test_change_offer_parentId_from_none_to_existing(client):
    response = await client.post(
        '/imports',
        json={
            'items': [
                {
                    'type': 'OFFER',
                    'name': 'Phyllis 10',
                    'id': '74b81fda-9cdc-4b63-8927-c978afed5cf4',
                    'parentId': '1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2',
                    'price': 10000,
                }
            ],
            'updateDate': '2027-01-01T10:00:00Z',
        },
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_existing_tree_with_id_8(client):

    response = await client.get(f'/nodes/{ROOT_ID}')

    assert response.status_code == 200
    response_json = response.json()
    logging.info('RESPONSE BEFORE: %s', response_json)
    deep_sort_children(response_json)
    logging.info('RESPONSE AFTER: %s', response_json)

    EXPECTED_TREE_2 = {
        'type': 'CATEGORY',
        'name': 'Товары',
        'id': '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1',
        'price': 42599,
        'parentId': None,
        'date': '2027-01-01T10:00:00.000Z',
        'children': [
            {
                'type': 'CATEGORY',
                'name': 'Телевизоры',
                'id': '1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2',
                'parentId': '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1',
                'price': 24333,
                'date': '2027-01-01T10:00:00.000Z',
                'children': [
                    {
                        'type': 'OFFER',
                        'name': "Samson 70\" LED UHD Smart",
                        'id': '98883e8f-0507-482f-bce2-2fb306cf6483',
                        'parentId': '1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2',
                        'price': 32999,
                        'date': '2022-02-03T12:00:00.000Z',
                        'children': None,
                    },
                    {
                        'type': 'OFFER',
                        'name': 'Phyllis 10',
                        'id': '74b81fda-9cdc-4b63-8927-c978afed5cf4',
                        'parentId': '1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2',
                        'price': 10000,
                        'date': '2027-01-01T10:00:00.000Z',
                        'children': None,
                    },
                    {
                        'type': 'OFFER',
                        'name': 'Update Readme 10',
                        'id': '73bc3b36-02d1-4245-ab35-3106c9ee1c65',
                        'parentId': '1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2',
                        'price': 30000,
                        'date': '2022-06-18T17:36:08.000Z',
                        'children': None,
                    },
                ],
            },
            {
                'type': 'CATEGORY',
                'name': 'Смартфоны',
                'id': 'd515e43f-f3f6-4471-bb77-6b455017a2d2',
                'parentId': '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1',
                'price': 69999,
                'date': '2022-02-02T12:00:00.000Z',
                'children': [
                    {
                        'type': 'OFFER',
                        'name': 'jPhone 13',
                        'id': '863e1a7a-1304-42ae-943b-179184c077e3',
                        'parentId': 'd515e43f-f3f6-4471-bb77-6b455017a2d2',
                        'price': 79999,
                        'date': '2022-02-02T12:00:00.000Z',
                        'children': None,
                    },
                    {
                        'type': 'OFFER',
                        'name': 'Xomiа Readme 10',
                        'id': 'b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4',
                        'parentId': 'd515e43f-f3f6-4471-bb77-6b455017a2d2',
                        'price': 59999,
                        'date': '2022-02-02T12:00:00.000Z',
                        'children': None,
                    },
                ],
            },
        ],
    }

    deep_sort_children(EXPECTED_TREE_2)
    print_diff(EXPECTED_TREE_2, response_json)
    assert (
        response_json == EXPECTED_TREE_2
    ), "Response tree doesn't match expected tree"


@pytest.mark.asyncio
async def test_change_category_parentId_1(client):
    response = await client.post(
        '/imports',
        json={
            'items': [
                {
                    'type': 'CATEGORY',
                    'name': 'Телевизоры',
                    'id': '1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2',
                    'parentId': 'd515e43f-f3f6-4471-bb77-6b455017a2d2',
                }
            ],
            'updateDate': '2028-01-01T10:00:00Z',
        },
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_existing_tree_with_id_9(client):

    response = await client.get(f'/nodes/{ROOT_ID}')

    assert response.status_code == 200
    response_json = response.json()
    logging.info('RESPONSE BEFORE: %s', response_json)
    deep_sort_children(response_json)
    logging.info('RESPONSE AFTER: %s', response_json)

    EXPECTED_TREE_2 = {
        'type': 'CATEGORY',
        'name': 'Товары',
        'id': '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1',
        'price': 42599,
        'parentId': None,
        'date': '2028-01-01T10:00:00.000Z',
        'children': [
            {
                'type': 'CATEGORY',
                'name': 'Смартфоны',
                'id': 'd515e43f-f3f6-4471-bb77-6b455017a2d2',
                'parentId': '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1',
                'price': 42599,
                'date': '2028-01-01T10:00:00.000Z',
                'children': [
                    {
                        'type': 'CATEGORY',
                        'name': 'Телевизоры',
                        'id': '1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2',
                        'parentId': 'd515e43f-f3f6-4471-bb77-6b455017a2d2',
                        'price': 24333,
                        'date': '2028-01-01T10:00:00.000Z',
                        'children': [
                            {
                                'type': 'OFFER',
                                'name': "Samson 70\" LED UHD Smart",
                                'id': '98883e8f-0507-482f-bce2-2fb306cf6483',
                                'parentId': '1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2',
                                'price': 32999,
                                'date': '2022-02-03T12:00:00.000Z',
                                'children': None,
                            },
                            {
                                'type': 'OFFER',
                                'name': 'Phyllis 10',
                                'id': '74b81fda-9cdc-4b63-8927-c978afed5cf4',
                                'parentId': '1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2',
                                'price': 10000,
                                'date': '2027-01-01T10:00:00.000Z',
                                'children': None,
                            },
                            {
                                'type': 'OFFER',
                                'name': 'Update Readme 10',
                                'id': '73bc3b36-02d1-4245-ab35-3106c9ee1c65',
                                'parentId': '1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2',
                                'price': 30000,
                                'date': '2022-06-18T17:36:08.000Z',
                                'children': None,
                            },
                        ],
                    },
                    {
                        'type': 'OFFER',
                        'name': 'jPhone 13',
                        'id': '863e1a7a-1304-42ae-943b-179184c077e3',
                        'parentId': 'd515e43f-f3f6-4471-bb77-6b455017a2d2',
                        'price': 79999,
                        'date': '2022-02-02T12:00:00.000Z',
                        'children': None,
                    },
                    {
                        'type': 'OFFER',
                        'name': 'Xomiа Readme 10',
                        'id': 'b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4',
                        'parentId': 'd515e43f-f3f6-4471-bb77-6b455017a2d2',
                        'price': 59999,
                        'date': '2022-02-02T12:00:00.000Z',
                        'children': None,
                    },
                ],
            },
        ],
    }

    deep_sort_children(EXPECTED_TREE_2)
    print_diff(EXPECTED_TREE_2, response_json)
    assert (
        response_json == EXPECTED_TREE_2
    ), "Response tree doesn't match expected tree"


@pytest.mark.asyncio
async def test_change_category_parentId_2(client):
    response = await client.post(
        '/imports',
        json={
            'items': [
                {
                    'type': 'CATEGORY',
                    'name': 'Телевизоры',
                    'id': '1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2',
                    'parentId': '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1',
                }
            ],
            'updateDate': '2029-01-01T10:00:00Z',
        },
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_existing_tree_with_id_10(client):

    response = await client.get(f'/nodes/{ROOT_ID}')

    assert response.status_code == 200
    response_json = response.json()
    logging.info('RESPONSE BEFORE: %s', response_json)
    deep_sort_children(response_json)
    logging.info('RESPONSE AFTER: %s', response_json)

    EXPECTED_TREE_2 = {
        'type': 'CATEGORY',
        'name': 'Товары',
        'id': '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1',
        'price': 42599,
        'parentId': None,
        'date': '2029-01-01T10:00:00.000Z',
        'children': [
            {
                'type': 'CATEGORY',
                'name': 'Телевизоры',
                'id': '1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2',
                'parentId': '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1',
                'price': 24333,
                'date': '2029-01-01T10:00:00.000Z',
                'children': [
                    {
                        'type': 'OFFER',
                        'name': "Samson 70\" LED UHD Smart",
                        'id': '98883e8f-0507-482f-bce2-2fb306cf6483',
                        'parentId': '1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2',
                        'price': 32999,
                        'date': '2022-02-03T12:00:00.000Z',
                        'children': None,
                    },
                    {
                        'type': 'OFFER',
                        'name': 'Phyllis 10',
                        'id': '74b81fda-9cdc-4b63-8927-c978afed5cf4',
                        'parentId': '1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2',
                        'price': 10000,
                        'date': '2027-01-01T10:00:00.000Z',
                        'children': None,
                    },
                    {
                        'type': 'OFFER',
                        'name': 'Update Readme 10',
                        'id': '73bc3b36-02d1-4245-ab35-3106c9ee1c65',
                        'parentId': '1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2',
                        'price': 30000,
                        'date': '2022-06-18T17:36:08.000Z',
                        'children': None,
                    },
                ],
            },
            {
                'type': 'CATEGORY',
                'name': 'Смартфоны',
                'id': 'd515e43f-f3f6-4471-bb77-6b455017a2d2',
                'parentId': '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1',
                'price': 69999,
                'date': '2029-01-01T10:00:00.000Z',
                'children': [
                    {
                        'type': 'OFFER',
                        'name': 'jPhone 13',
                        'id': '863e1a7a-1304-42ae-943b-179184c077e3',
                        'parentId': 'd515e43f-f3f6-4471-bb77-6b455017a2d2',
                        'price': 79999,
                        'date': '2022-02-02T12:00:00.000Z',
                        'children': None,
                    },
                    {
                        'type': 'OFFER',
                        'name': 'Xomiа Readme 10',
                        'id': 'b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4',
                        'parentId': 'd515e43f-f3f6-4471-bb77-6b455017a2d2',
                        'price': 59999,
                        'date': '2022-02-02T12:00:00.000Z',
                        'children': None,
                    },
                ],
            },
        ],
    }

    deep_sort_children(EXPECTED_TREE_2)
    print_diff(EXPECTED_TREE_2, response_json)
    assert (
        response_json == EXPECTED_TREE_2
    ), "Response tree doesn't match expected tree"


@pytest.mark.asyncio
async def test_change_offer_parentId_3(client):
    response = await client.post(
        '/imports',
        json={
            'items': [
                {
                    'type': 'OFFER',
                    'name': 'Update Readme 11',
                    'id': '73bc3b36-02d1-4245-ab35-3106c9ee1c65',
                    'price': 1,
                    'parentId': None,
                }
            ],
            'updateDate': '2030-01-01T10:00:00Z',
        },
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_import_new_root_1(client):
    response = await client.post(
        '/imports',
        json={
            'items': [
                {
                    'type': 'CATEGORY',
                    'name': 'ВСЕ ТОВАРЫ',
                    'id': '11111111-bbdd-47d3-ad8f-82ef4c269df1',
                    'parentId': None,
                }
            ],
            'updateDate': '2032-01-01T10:00:00Z',
        },
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_update_ROOT_ID(client):
    response = await client.post(
        '/imports',
        json={
            'items': [
                {
                    'type': 'CATEGORY',
                    'name': 'Товары',
                    'id': f'{ROOT_ID}',
                    'parentId': '11111111-bbdd-47d3-ad8f-82ef4c269df1',
                }
            ],
            'updateDate': '2033-01-01T10:00:00Z',
        },
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_change_offer_parentId_4(client):
    response = await client.post(
        '/imports',
        json={
            'items': [
                {
                    'type': 'OFFER',
                    'name': 'Update Readme 11',
                    'id': '73bc3b36-02d1-4245-ab35-3106c9ee1c65',
                    'price': 2,
                    'parentId': 'd515e43f-f3f6-4471-bb77-6b455017a2d2',
                }
            ],
            'updateDate': '2034-01-01T10:00:00Z',
        },
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_existing_tree_with_id_11(client):
    response = await client.get('/nodes/11111111-bbdd-47d3-ad8f-82ef4c269df1')
    assert response.status_code == 200
    response_json = response.json()
    EXPECTED_TREE_3 = {
        'type': 'CATEGORY',
        'name': 'ВСЕ ТОВАРЫ',
        'id': '11111111-bbdd-47d3-ad8f-82ef4c269df1',
        'parentId': None,
        'price': 36599,
        'date': '2034-01-01T10:00:00.000Z',
        'children': [
            {
                'type': 'CATEGORY',
                'name': 'Товары',
                'id': '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1',
                'price': 36599,
                'parentId': '11111111-bbdd-47d3-ad8f-82ef4c269df1',
                'date': '2034-01-01T10:00:00.000Z',
                'children': [
                    {
                        'type': 'CATEGORY',
                        'name': 'Телевизоры',
                        'id': '1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2',
                        'parentId': '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1',
                        'price': 21499,
                        'date': '2030-01-01T10:00:00.000Z',
                        'children': [
                            {
                                'type': 'OFFER',
                                'name': "Samson 70\" LED UHD Smart",
                                'id': '98883e8f-0507-482f-bce2-2fb306cf6483',
                                'parentId': '1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2',
                                'price': 32999,
                                'date': '2022-02-03T12:00:00.000Z',
                                'children': None,
                            },
                            {
                                'type': 'OFFER',
                                'name': 'Phyllis 10',
                                'id': '74b81fda-9cdc-4b63-8927-c978afed5cf4',
                                'parentId': '1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2',
                                'price': 10000,
                                'date': '2027-01-01T10:00:00.000Z',
                                'children': None,
                            },
                        ],
                    },
                    {
                        'type': 'CATEGORY',
                        'name': 'Смартфоны',
                        'id': 'd515e43f-f3f6-4471-bb77-6b455017a2d2',
                        'parentId': '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1',
                        'price': 46666,
                        'date': '2034-01-01T10:00:00.000Z',
                        'children': [
                            {
                                'type': 'OFFER',
                                'name': 'Update Readme 11',
                                'id': '73bc3b36-02d1-4245-ab35-3106c9ee1c65',
                                'parentId': 'd515e43f-f3f6-4471-bb77-6b455017a2d2',
                                'price': 2,
                                'date': '2034-01-01T10:00:00.000Z',
                                'children': None,
                            },
                            {
                                'type': 'OFFER',
                                'name': 'jPhone 13',
                                'id': '863e1a7a-1304-42ae-943b-179184c077e3',
                                'parentId': 'd515e43f-f3f6-4471-bb77-6b455017a2d2',
                                'price': 79999,
                                'date': '2022-02-02T12:00:00.000Z',
                                'children': None,
                            },
                            {
                                'type': 'OFFER',
                                'name': 'Xomiа Readme 10',
                                'id': 'b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4',
                                'parentId': 'd515e43f-f3f6-4471-bb77-6b455017a2d2',
                                'price': 59999,
                                'date': '2022-02-02T12:00:00.000Z',
                                'children': None,
                            },
                        ],
                    },
                ],
            }
        ],
    }
    deep_sort_children(response_json)
    deep_sort_children(EXPECTED_TREE_3)
    print_diff(EXPECTED_TREE_3, response_json)
    assert (
        response_json == EXPECTED_TREE_3
    ), "Response tree doesn't match expected tree"


@pytest.mark.asyncio
async def test_delete_offer_in_category_1(client):
    response = await client.delete(
        '/delete/98883e8f-0507-482f-bce2-2fb306cf6483'
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_existing_tree_with_id_12(client):
    response = await client.get('/nodes/11111111-bbdd-47d3-ad8f-82ef4c269df1')
    assert response.status_code == 200
    response_json = response.json()
    EXPECTED_TREE_3 = {
        'type': 'CATEGORY',
        'name': 'ВСЕ ТОВАРЫ',
        'id': '11111111-bbdd-47d3-ad8f-82ef4c269df1',
        'parentId': None,
        'price': 37500,
        'date': '2034-01-01T10:00:00.000Z',
        'children': [
            {
                'type': 'CATEGORY',
                'name': 'Товары',
                'id': '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1',
                'price': 37500,
                'parentId': '11111111-bbdd-47d3-ad8f-82ef4c269df1',
                'date': '2034-01-01T10:00:00.000Z',
                'children': [
                    {
                        'type': 'CATEGORY',
                        'name': 'Телевизоры',
                        'id': '1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2',
                        'parentId': '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1',
                        'price': 10000,
                        'date': '2030-01-01T10:00:00.000Z',
                        'children': [
                            {
                                'type': 'OFFER',
                                'name': 'Phyllis 10',
                                'id': '74b81fda-9cdc-4b63-8927-c978afed5cf4',
                                'parentId': '1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2',
                                'price': 10000,
                                'date': '2027-01-01T10:00:00.000Z',
                                'children': None,
                            },
                        ],
                    },
                    {
                        'type': 'CATEGORY',
                        'name': 'Смартфоны',
                        'id': 'd515e43f-f3f6-4471-bb77-6b455017a2d2',
                        'parentId': '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1',
                        'price': 46666,
                        'date': '2034-01-01T10:00:00.000Z',
                        'children': [
                            {
                                'type': 'OFFER',
                                'name': 'Update Readme 11',
                                'id': '73bc3b36-02d1-4245-ab35-3106c9ee1c65',
                                'parentId': 'd515e43f-f3f6-4471-bb77-6b455017a2d2',
                                'price': 2,
                                'date': '2034-01-01T10:00:00.000Z',
                                'children': None,
                            },
                            {
                                'type': 'OFFER',
                                'name': 'jPhone 13',
                                'id': '863e1a7a-1304-42ae-943b-179184c077e3',
                                'parentId': 'd515e43f-f3f6-4471-bb77-6b455017a2d2',
                                'price': 79999,
                                'date': '2022-02-02T12:00:00.000Z',
                                'children': None,
                            },
                            {
                                'type': 'OFFER',
                                'name': 'Xomiа Readme 10',
                                'id': 'b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4',
                                'parentId': 'd515e43f-f3f6-4471-bb77-6b455017a2d2',
                                'price': 59999,
                                'date': '2022-02-02T12:00:00.000Z',
                                'children': None,
                            },
                        ],
                    },
                ],
            }
        ],
    }
    deep_sort_children(response_json)
    deep_sort_children(EXPECTED_TREE_3)
    print_diff(EXPECTED_TREE_3, response_json)
    assert (
        response_json == EXPECTED_TREE_3
    ), "Response tree doesn't match expected tree"


@pytest.mark.asyncio
async def test_delete_category_in_category_1(client):
    response = await client.delete(
        '/delete/d515e43f-f3f6-4471-bb77-6b455017a2d2'
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_existing_tree_with_id_13(client):
    response = await client.get('/nodes/11111111-bbdd-47d3-ad8f-82ef4c269df1')
    assert response.status_code == 200
    response_json = response.json()
    EXPECTED_TREE_3 = {
        'type': 'CATEGORY',
        'name': 'ВСЕ ТОВАРЫ',
        'id': '11111111-bbdd-47d3-ad8f-82ef4c269df1',
        'parentId': None,
        'price': 10000,
        'date': '2034-01-01T10:00:00.000Z',
        'children': [
            {
                'type': 'CATEGORY',
                'name': 'Товары',
                'id': '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1',
                'price': 10000,
                'parentId': '11111111-bbdd-47d3-ad8f-82ef4c269df1',
                'date': '2034-01-01T10:00:00.000Z',
                'children': [
                    {
                        'type': 'CATEGORY',
                        'name': 'Телевизоры',
                        'id': '1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2',
                        'parentId': '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1',
                        'price': 10000,
                        'date': '2030-01-01T10:00:00.000Z',
                        'children': [
                            {
                                'type': 'OFFER',
                                'name': 'Phyllis 10',
                                'id': '74b81fda-9cdc-4b63-8927-c978afed5cf4',
                                'parentId': '1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2',
                                'price': 10000,
                                'date': '2027-01-01T10:00:00.000Z',
                                'children': None,
                            },
                        ],
                    },
                ],
            }
        ],
    }
    deep_sort_children(response_json)
    deep_sort_children(EXPECTED_TREE_3)
    print_diff(EXPECTED_TREE_3, response_json)
    assert (
        response_json == EXPECTED_TREE_3
    ), "Response tree doesn't match expected tree"


@pytest.mark.asyncio
async def test_delete_offer_in_category_2(client):
    response = await client.delete(
        '/delete/74b81fda-9cdc-4b63-8927-c978afed5cf4'
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_existing_tree_with_id_14(client):
    response = await client.get('/nodes/11111111-bbdd-47d3-ad8f-82ef4c269df1')
    assert response.status_code == 200
    response_json = response.json()
    EXPECTED_TREE_3 = {
        'type': 'CATEGORY',
        'name': 'ВСЕ ТОВАРЫ',
        'id': '11111111-bbdd-47d3-ad8f-82ef4c269df1',
        'parentId': None,
        'price': None,
        'date': '2034-01-01T10:00:00.000Z',
        'children': [
            {
                'type': 'CATEGORY',
                'name': 'Товары',
                'id': '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1',
                'price': None,
                'parentId': '11111111-bbdd-47d3-ad8f-82ef4c269df1',
                'date': '2034-01-01T10:00:00.000Z',
                'children': [
                    {
                        'type': 'CATEGORY',
                        'name': 'Телевизоры',
                        'id': '1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2',
                        'parentId': '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1',
                        'price': None,
                        'date': '2030-01-01T10:00:00.000Z',
                        'children': [],
                    },
                ],
            }
        ],
    }
    deep_sort_children(response_json)
    deep_sort_children(EXPECTED_TREE_3)
    print_diff(EXPECTED_TREE_3, response_json)
    assert (
        response_json == EXPECTED_TREE_3
    ), "Response tree doesn't match expected tree"


@pytest.mark.asyncio
async def test_delete_offer_in_category_3(client):
    response = await client.delete(
        '/delete/11111111-bbdd-47d3-ad8f-82ef4c269df1'
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_existing_tree_with_id_15(client):
    response = await client.get('/nodes/11111111-bbdd-47d3-ad8f-82ef4c269df1')
    assert response.status_code == 404
