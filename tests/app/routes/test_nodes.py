# encoding=utf8
import logging
import json
import subprocess

import pytest

logging.getLogger("uvicorn.error")

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
async def test_get_tree_with_id(client):

    response = await client.get(f'/nodes/{ROOT_ID}')

    assert response.status_code == 200
    response_json = response.json()
    logging.info("RESPONSE BEFORE: %s", response_json)
    deep_sort_children(response_json)
    logging.info("RESPONSE AFTER: %s", response_json)

    deep_sort_children(EXPECTED_TREE)
    print_diff(EXPECTED_TREE, response_json)
    # assert response_json == EXPECTED_TREE, "Response tree doesn't match expected tree"



def deep_sort_children(node):
    if node.get("children"):
        node["children"].sort(key=lambda x: x["id"])

        for child in node["children"]:
            deep_sort_children(child)

def print_diff(expected, response):
    with open("expected.json", "w") as f:
        json.dump(expected, f, indent=2, ensure_ascii=False, sort_keys=True)
        f.write("\n")

    with open("response.json", "w") as f:
        json.dump(response, f, indent=2, ensure_ascii=False, sort_keys=True)
        f.write("\n")

    subprocess.run(["git", "--no-pager", "diff", "--no-index",
                    "expected.json", "response.json"])
