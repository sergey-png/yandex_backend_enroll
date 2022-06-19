import logging
from typing import Any, Optional

from db.init import create_session
from db.models import Item
from db.viewshopunit import ShopUnitView

logger = logging.getLogger("uvicorn.error")


def create_element(**data: Any) -> bool:
    logger.info('*START*')
    with create_session() as session:
        logger.info('Data received: "%s"', data)
        item = Item(**data)
        if item.id == item.parentId:
            logger.info('Item cannot be parent of itself')
            return False
        # check if item with same id exists
        if session.query(Item).filter(Item.id == item.id).first():
            logger.info('Item with id "%s" already exists', item.id)
            # check if item with parentId exists
            if item.parentId:
                logger.info('This Item with parentId "%s"', item.parentId)
                if not session.query(Item).filter(Item.id == item.parentId).first():
                    return False
                    # raise Exception('Parent item with id "%s" not found' % item.parentId)
            session.query(Item).filter(Item.id == item.id).update(data)
        else:
            logger.info('Item with id "%s" does not exist', item.id)
            if item.parentId:
                logger.info('This Item with parentId "%s"', item.parentId)
                if not session.query(Item).filter(Item.id == item.parentId).first():
                    return False
                    # raise Exception('Parent item with id "%s" not found' % item.parentId)
            session.add(item)
        return True


def delete_element(item_id: str) -> bool:
    logger.info('*START*')
    with create_session() as session:
        logger.info('Item id received: %s', item_id)
        item = session.query(Item).filter(Item.id == item_id).first()
        if item:
            logger.info('Item with id %s found', item_id)
            session.delete(item)
            return True
        else:
            logger.info('Item with id %s not found', item_id)
            return False


"""
def get_element_with_id(item_id: str, session: Any) -> Optional[Item]:
    logger.info('*START*')
    logger.info('Item id received: %s', item_id)
    list_items = []
    list_items = get_all_elements(item_id, session, list_items)
    logger.info('List of ITEMS: %s', list_items)
    if list_items:
        return list_items
    return None


def get_all_elements(item_id: str, session: Any, list_items: list) -> list:
    item: Item = session.query(Item).filter(Item.id == item_id).first()
    if item:
        return item
        # if item.children:
        #     for child in item.children:
        #         list_items = get_all_elements(child.id, session, list_items)
    return None  # list_items
"""


def get_one_element(item_id: str) -> Optional[list]:
    with create_session() as session:
        item = session.query(Item).filter(Item.id == item_id).first()
        if item:
            result_values = ShopUnitView(item)
            logger.info('RESULT_VALUES CHILDREN ID = %s', result_values.children)
            return result_values
        return None
