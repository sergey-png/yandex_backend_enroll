# import logging
#
# import pytest
#
# from db.init import create_session
# from db.models import Item
#
# logging.getLogger('uvicorn.error')
#
#
# def test_create_session():
#     with create_session() as session:
#         assert session is not None
#
#
# def test_create_session_twice():
#     with create_session() as session:
#         assert session is not None
#     with create_session() as session:
#         assert session is not None
#
#
# def test_create_session_and_rise_exception():
#     with pytest.raises(Exception):
#         with create_session() as session:
#             assert session is not None
#             raise Exception('test')
#
#
# def test_create_Item_and_copy():
#     with create_session() as session:
#         item = Item(name='test')
#         session.add(item)
#         session.rollback()
#         item_copy = item.copy(with_children=True)
#         assert item_copy.id == item.id
#         assert item_copy.name == item.name
