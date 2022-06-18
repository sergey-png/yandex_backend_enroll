import logging

from db.init import create_session
from db.models import Item

logger = logging.getLogger(__name__)


def create_element(**data):
    logger.info('*START*')
    with create_session() as session:
        logger.info('Data received: %s', data)
        item = Item(**data)

        # check if item with same id exists
        if session.query(Item).filter(Item.id == item.id).first():
            logger.info('Item with id %s already exists', item.id)
            session.query(Item).filter(Item.id == item.id).update(data)
        else:
            logger.info('Item with id %s does not exist', item.id)
            session.add(item)
