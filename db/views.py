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
        item_to_change = Item(**data)
        if item_to_change.id == item_to_change.parentId:
            logger.info('Item cannot be parent of itself')
            return False

        # check if item_to_change with same id exists in db
        found_item = session.query(Item).filter(Item.id == item_to_change.id).first()
        if found_item:
            logger.info('Item with id "%s" already exists', item_to_change.id)
            # check if item_to_change with parentId
            if item_to_change.parentId:
                logger.info('This Item with parentId "%s"', item_to_change.parentId)
                # check if parentId exists
                if not session.query(Item).filter(Item.id == item_to_change.parentId).first():
                    # raise Exception('Parent item_to_change with id "%s" not found' % item_to_change.parentId)
                    return False  # parentId does not exist in DB

                # check if item_to_change changes parentId
                if found_item.parentId == item_to_change.parentId:
                    logger.info('Found Item with parentId "%s" has no difference with item_to_change parentId "%s"',
                                found_item.parentId, item_to_change.parentId)
                    session.query(Item).filter(Item.id == item_to_change.id).update(data)

                else:
                    logger.info('Found Item with different parentId "%s" that changes self parentId to "%s"',
                                found_item.parentId, item_to_change.parentId)
                    session.query(Item).filter(Item.id == item_to_change.id).update(data)

            # TODO update all parents of this item_to_change

        else:
            item_to_add = item_to_change
            logger.info('Item with id "%s" does not exist. Creating new one...', item_to_add.id)
            # check if item_to_change with parentId
            if item_to_add.parentId:
                logger.info('This Item with parentId "%s"', item_to_add.parentId)
                if not session.query(Item).filter(Item.id == item_to_add.parentId).first():
                    return False
                    # raise Exception('Parent item_to_change with id "%s" not found' % item_to_change.parentId)
                if item_to_add.type == 'CATEGORY':
                    item_to_add.all_price = 0
                    item_to_add.count_items = 0
                    item_to_add.price = 0
                elif item_to_add.type == 'OFFER':
                    item_to_add.all_price = None
                    item_to_add.count_items = 1

                session.add(item_to_add)
                # update all parents of this item_to_change
                while True:
                    parent_item = session.query(Item).filter(Item.id == item_to_add.parentId).first()
                    if parent_item:
                        if parent_item.type == 'CATEGORY' and item_to_add.type == 'OFFER':
                            parent_item.all_price += item_to_add.price
                            parent_item.count_items += item_to_add.count_items
                            parent_item.date = item_to_add.date
                            if parent_item.count_items == 0:
                                parent_item.price = 0
                            else:
                                parent_item.price = parent_item.all_price // parent_item.count_items

                            session.query(Item).filter(Item.id == parent_item.id).update(
                                dict(all_price=parent_item.all_price,
                                     count_items=parent_item.count_items,
                                     date=parent_item.date,
                                     price=parent_item.price))
                        elif parent_item.type == 'OFFER' and item_to_add.type == 'OFFER':
                            logger.info("Parent item is OFFER as well as item_to_add, ERROR")
                            return False
                        elif parent_item.type == 'OFFER' and item_to_add.type == 'CATEGORY':
                            logger.info("Parent item is OFFER, but item_to_add is CATEGORY, ERROR")
                            return False
                        elif parent_item.type == 'CATEGORY' and item_to_add.type == 'CATEGORY':

                            parent_item.all_price = 0
                            parent_item.count_items = 0
                            for child in parent_item.children:
                                if child.type == 'CATEGORY':
                                    parent_item.all_price += child.all_price
                                elif child.type == 'OFFER':
                                    parent_item.all_price += child.price
                                parent_item.count_items += child.count_items

                            parent_item.date = item_to_add.date
                            if parent_item.count_items == 0:
                                parent_item.price = 0
                            else:
                                parent_item.price = parent_item.all_price // parent_item.count_items

                            session.query(Item).filter(Item.id == parent_item.id).update(
                                dict(all_price=parent_item.all_price,
                                     count_items=parent_item.count_items,
                                     date=parent_item.date,
                                     price=parent_item.price))
                        item_to_add = parent_item
                    else:
                        break

            else:
                logger.info('This Item has no parentId')
                if item_to_add.type == 'CATEGORY':
                    logger.info('This Item is a CATEGORY')
                    item_to_add.all_price = 0
                    item_to_add.count_items = 0
                    item_to_add.price = 0
                elif item_to_add.type == 'OFFER':
                    logger.info('This Item is an OFFER')
                    item_to_add.all_price = None
                    item_to_add.count_items = 1
                session.add(item_to_add)

            # TODO update all parents of this item_to_change
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
