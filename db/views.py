import logging
from typing import Any, Optional

from db.init import create_session
from db.models import Item
from db.viewshopunit import ShopUnitView
from collections import defaultdict

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
        found_item: Item = session.query(Item).filter(Item.id == item_to_change.id).first()
        if found_item:
            logger.info('Item with id "%s" already exists', item_to_change.id)
            # check if item_to_change with parentId
            if item_to_change.parentId:
                logger.info('This Item with parentId "%s"', item_to_change.parentId)
                # check if parentId exists in db
                if not session.query(Item).filter(Item.id == item_to_change.parentId).first():  # Done
                    # raise Exception('Parent item_to_change with id "%s" not found' % item_to_change.parentId)
                    return False  # parentId does not exist in DB

                # check if item_to_change changes parentId
                if found_item.parentId == item_to_change.parentId:
                    # parentId is the same, so update item_to_change

                    update_item_parentId_without_changes(session, item_to_change, found_item, data)

                else:
                    # parentIds are different

                    if found_item.parentId is not None:  # parentId is not None
                        original_item_to_change = item_to_change.copy()

                        item_to_change.parentId = None

                        # something -> None
                        update_item_parentID_to_None(session, found_item, item_to_change, data)
                        # None -> something
                        update_item_parentId_from_None_to_something(session, found_item, original_item_to_change, data)


                    elif found_item.parentId is None:
                        # when found_item change parentId: None -> something
                        update_item_parentId_from_None_to_something(session, found_item, item_to_change, data)
            else:
                # when found_item change parentId: something -> None and updates itself
                update_item_parentID_to_None(session, found_item, item_to_change, data)

        else:
            if add_element(session, item_to_change, data) is False:
                return False
        return True


def delete_element(item_id: str) -> bool:
    logger.info('*START*')
    with create_session() as session:
        logger.info('Item id received: %s', item_id)
        item = session.query(Item).filter(Item.id == item_id).first()
        if item:
            logger.info('Item with id %s found', item_id)
            return delete_item(session, item)
        else:
            logger.info('Item with id %s not found', item_id)
            return False


def get_one_element(item_id: str) -> Optional[list]:
    with create_session() as session:
        item = session.query(Item).filter(Item.id == item_id).first()
        if item:
            result_values = ShopUnitView(item)
            logger.info('RESULT_VALUES CHILDREN ID = %s', result_values.children)
            return result_values
        return None


# delete item
def delete_item(session: Any, item_to_delete: Item) -> bool:
    if item_to_delete.parentId is None:
        logger.info('Item with id "%s" has no parentId', item_to_delete.id)
        session.delete(item_to_delete)
    else:

        update_item_parentId_to_None_after_deleting(session, item_to_delete, item_to_delete)










        session.delete(item_to_delete)
    return True


# when item_to_change updates and parentId doesn't change
def update_item_parentId_without_changes(session: Any, item_to_change: Item, found_item: Item,
                                         data: dict[str, Any]) -> bool:
    new_data_for_others = defaultdict(dict[str, Any])

    if item_to_change.type == "OFFER":
        new_data_for_others['price'] = item_to_change.price - found_item.price

        session.query(Item).filter(Item.id == item_to_change.id).update(data)

        # update all parents of this item_to_change
        while True:
            parent_item = session.query(Item).filter(Item.id == item_to_change.parentId).first()
            if parent_item:
                if parent_item.type == 'CATEGORY' and item_to_change.type == 'OFFER':
                    parent_item.all_price += new_data_for_others['price']

                    parent_item.date = data['date']

                    parent_item.price = parent_item.all_price // parent_item.count_items \
                        if parent_item.count_items else None

                    session.query(Item).filter(Item.id == parent_item.id).update(
                        dict(all_price=parent_item.all_price,
                             date=parent_item.date,
                             price=parent_item.price))
                elif parent_item.type == 'CATEGORY' and item_to_change.type == 'CATEGORY':

                    parent_item.all_price += new_data_for_others['price']

                    parent_item.date = data['date']

                    parent_item.price = parent_item.all_price // parent_item.count_items \
                        if parent_item.count_items else None

                    session.query(Item).filter(Item.id == parent_item.id).update(
                        dict(all_price=parent_item.all_price,
                             date=parent_item.date,
                             price=parent_item.price))
                item_to_change = parent_item
            else:
                break
    elif item_to_change.type == "CATEGORY":
        session.query(Item).filter(Item.id == item_to_change.id).update(data)
        item_to_change = session.query(Item).filter(Item.id == item_to_change.id).first()
        item_to_change.price = item_to_change.all_price // item_to_change.count_items \
            if item_to_change.count_items else None
        session.query(Item).filter(Item.id == item_to_change.id).update(
            dict(
                price=item_to_change.price,
                date=item_to_change.date,
            )
        )

        # update all parents of this item_to_change
        while True:
            parent_item = session.query(Item).filter(Item.id == item_to_change.parentId).first()
            if parent_item:
                if parent_item.type == 'CATEGORY' and item_to_change.type == 'CATEGORY':
                    parent_item.date = data['date']
                    session.query(Item).filter(Item.id == parent_item.id).update(
                        dict(date=parent_item.date))
                item_to_change = parent_item
            else:
                break
    return True


# when found_item change parentId: None -> something
def update_item_parentId_from_None_to_something(session: Any, found_item: Item, item_to_change: Item,
                                                data: dict[str, Any]) -> bool:
    session.query(Item).filter(Item.id == item_to_change.id).update(data)
    if item_to_change.type == "OFFER":
        found_item_original = session.query(Item).filter(Item.id == item_to_change.id).first()
        found_item = found_item_original
        while True:
            parent_item = session.query(Item).filter(Item.id == found_item.parentId).first()
            if parent_item:
                if parent_item.type == 'CATEGORY' and item_to_change.type == 'OFFER':
                    parent_item.all_price += found_item_original.price
                    parent_item.count_items += 1
                    parent_item.date = data['date']
                    parent_item.price = parent_item.all_price // parent_item.count_items \
                        if parent_item.count_items else None
                    session.query(Item).filter(Item.id == parent_item.id).update(
                        dict(all_price=parent_item.all_price,
                             count_items=parent_item.count_items,
                             date=parent_item.date,
                             price=parent_item.price)
                    )
                elif parent_item.type == 'CATEGORY' and item_to_change.type == 'CATEGORY':
                    parent_item.all_price += found_item_original.price
                    parent_item.count_items += 1
                    parent_item.date = data['date']
                    parent_item.price = parent_item.all_price // parent_item.count_items \
                        if parent_item.count_items else None
                    session.query(Item).filter(Item.id == parent_item.id).update(
                        dict(all_price=parent_item.all_price,
                             count_items=parent_item.count_items,
                             date=parent_item.date,
                             price=parent_item.price)
                    )
                found_item = parent_item
            else:
                break
    elif item_to_change.type == "CATEGORY":

        item_to_change.price = found_item.all_price // found_item.count_items \
            if found_item.count_items else None
        session.query(Item).filter(Item.id == item_to_change.id).update(
            dict(
                price=item_to_change.price,
            )
        )
        while True:
            parent_item = session.query(Item).filter(Item.id == item_to_change.parentId).first()
            if parent_item:
                if parent_item.type == 'CATEGORY' and item_to_change.type == 'CATEGORY':
                    parent_item.all_price += found_item.all_price
                    parent_item.count_items += found_item.count_items
                    parent_item.date = data['date']
                    parent_item.price = parent_item.all_price // parent_item.count_items \
                        if parent_item.count_items else None
                    session.query(Item).filter(Item.id == parent_item.id).update(
                        dict(all_price=parent_item.all_price,
                             count_items=parent_item.count_items,
                             date=parent_item.date,
                             price=parent_item.price)
                    )
                item_to_change = parent_item
            else:
                break
    return True


# when found_item change parentId -> None and updates itself
def update_item_parentID_to_None(session: Any, found_item: Item, item_to_change: Item, data: dict) -> bool:
    found_item_original = found_item.copy()
    if item_to_change.type == "OFFER":
        while True:
            parent_item = session.query(Item).filter(Item.id == found_item.parentId).first()
            if parent_item:
                if parent_item.type == 'CATEGORY' and found_item.type == 'OFFER':
                    parent_item.all_price -= found_item_original.price
                    parent_item.count_items -= 1
                    parent_item.date = data['date']
                    parent_item.price = parent_item.all_price // parent_item.count_items \
                        if parent_item.count_items else None

                    session.query(Item).filter(Item.id == parent_item.id).update(
                        dict(
                            all_price=parent_item.all_price,
                            count_items=parent_item.count_items,
                            date=parent_item.date,
                            price=parent_item.price)
                    )
                elif parent_item.type == 'CATEGORY' and found_item.type == 'CATEGORY':
                    parent_item.all_price -= found_item_original.price
                    parent_item.count_items -= 1
                    parent_item.date = data['date']
                    parent_item.price = parent_item.all_price // parent_item.count_items \
                        if parent_item.count_items else None

                    session.query(Item).filter(Item.id == parent_item.id).update(
                        dict(
                            all_price=parent_item.all_price,
                            count_items=parent_item.count_items,
                            date=parent_item.date,
                            price=parent_item.price)
                    )
                found_item = parent_item
            else:
                break

    elif item_to_change.type == "CATEGORY":
        if data['price'] is None:
            data['price'] = found_item_original.all_price // found_item_original.count_items \
                if found_item_original.count_items else None
        while True:
            parent_item = session.query(Item).filter(Item.id == found_item.parentId).first()
            if parent_item:
                if parent_item.type == 'CATEGORY' and found_item.type == 'CATEGORY':
                    parent_item.all_price -= found_item_original.all_price
                    parent_item.count_items -= found_item_original.count_items
                    parent_item.date = data['date']
                    parent_item.price = parent_item.all_price // parent_item.count_items \
                        if parent_item.count_items else None

                    session.query(Item).filter(Item.id == parent_item.id).update(
                        dict(
                            all_price=parent_item.all_price,
                            count_items=parent_item.count_items,
                            date=parent_item.date,
                            price=parent_item.price)
                    )
                    found_item = parent_item
            else:
                break

    session.query(Item).filter(Item.id == found_item_original.id).update(data)
    return True


def update_item_parentId_to_None_after_deleting(session: Any, found_item: Item, item_to_change: Item) -> bool:
    found_item_original = found_item.copy()
    if item_to_change.type == "OFFER":
        while True:
            parent_item = session.query(Item).filter(Item.id == found_item.parentId).first()
            if parent_item:
                if parent_item.type == 'CATEGORY' and found_item.type == 'OFFER':
                    parent_item.all_price -= found_item_original.price
                    parent_item.count_items -= 1
                    parent_item.price = parent_item.all_price // parent_item.count_items \
                        if parent_item.count_items else None

                    session.query(Item).filter(Item.id == parent_item.id).update(
                        dict(
                            all_price=parent_item.all_price,
                            count_items=parent_item.count_items,
                            price=parent_item.price
                        )
                    )
                elif parent_item.type == 'CATEGORY' and found_item.type == 'CATEGORY':
                    parent_item.all_price -= found_item_original.price
                    parent_item.count_items -= 1
                    parent_item.price = parent_item.all_price // parent_item.count_items \
                        if parent_item.count_items else None


                    session.query(Item).filter(Item.id == parent_item.id).update(
                        dict(
                            all_price=parent_item.all_price,
                            count_items=parent_item.count_items,
                            price=parent_item.price
                        )
                    )
                found_item = parent_item
            else:
                break

    elif item_to_change.type == "CATEGORY":
        # if  is None:
        #     data['price'] = found_item_original.all_price // found_item_original.count_items \
        #         if found_item_original.count_items else None
        while True:
            parent_item = session.query(Item).filter(Item.id == found_item.parentId).first()
            if parent_item:
                if parent_item.type == 'CATEGORY' and found_item.type == 'CATEGORY':
                    parent_item.all_price -= found_item_original.all_price
                    parent_item.count_items -= found_item_original.count_items
                    parent_item.price = parent_item.all_price // parent_item.count_items \
                        if parent_item.count_items else None


                    session.query(Item).filter(Item.id == parent_item.id).update(
                        dict(
                            all_price=parent_item.all_price,
                            count_items=parent_item.count_items,
                            price=parent_item.price
                        )
                    )
                    found_item = parent_item
            else:
                break
    return True

def add_element(session: Any, item_to_add: Item, data: dict[str, Any]) -> bool:
    logger.info('*START*')
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
            item_to_add.price = None
        elif item_to_add.type == 'OFFER':
            item_to_add.all_price = None
            item_to_add.count_items = 1

        session.add(item_to_add)
        # update all parents of this item_to_change
        update_all_parents_1(session, item_to_add, data)

    else:
        logger.info('This Item has no parentId')
        if item_to_add.type == 'CATEGORY':
            logger.info('This Item is a CATEGORY')
            item_to_add.all_price = 0
            item_to_add.count_items = 0
            item_to_add.price = None
        elif item_to_add.type == 'OFFER':
            logger.info('This Item is an OFFER')
            item_to_add.all_price = None
            item_to_add.count_items = 1
        session.add(item_to_add)
    return True


def update_all_parents_1(session: Any, item_to_add: Item, data: dict[str, Any]) -> bool:
    while True:
        parent_item = session.query(Item).filter(Item.id == item_to_add.parentId).first()
        if parent_item:
            if parent_item.type == 'CATEGORY' and item_to_add.type == 'OFFER':
                parent_item.all_price += item_to_add.price
                parent_item.count_items += item_to_add.count_items
                parent_item.date = data['date']
                parent_item.price = parent_item.all_price // parent_item.count_items \
                    if parent_item.count_items else None

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

                parent_item.date = data['date']
                parent_item.price = parent_item.all_price // parent_item.count_items \
                    if parent_item.count_items else None

                session.query(Item).filter(Item.id == parent_item.id).update(
                    dict(all_price=parent_item.all_price,
                         count_items=parent_item.count_items,
                         date=parent_item.date,
                         price=parent_item.price))
            item_to_add = parent_item
        else:
            return True
