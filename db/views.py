import logging

from db.init import create_session
from db.models import Item

logger = logging.getLogger(__name__)


def create_element(**data):
    logger.info('*START**')
    with create_session() as session:
        logger.info('Data received: %s', data)
        item = Item(**data)
        session.add(item)
        logger.info('Successfully added item: %s', item)
