from db.init import create_session
from db.models import Item


def create_element(**data):
    with create_session() as session:
        item = Item(**data)
        session.add(item)
