import logging
from typing import Any

from db.init import create_session
from db.models import Item

logger = logging.getLogger(__name__)


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

