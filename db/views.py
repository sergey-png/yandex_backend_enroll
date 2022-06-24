import logging
from typing import Any, Optional
from db.init import create_session
from db.models import Item
from db.models import Stats
from db.viewshopunit import ShopUnitView
from collections import defaultdict
from datetime import datetime
from datetime import timedelta
from datetime import timezone

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


def update_statistics(session: Any, item_to_update_id: str) -> bool:
    session.commit()
    item_to_update = session.query(Item).filter(Item.id == item_to_update_id).first()
    if item_to_update:
        items = session.query(Stats).filter(Stats.id == item_to_update_id, Stats.date != item_to_update.date).all()
        if items:
            for item in items:
                session.query(Stats).filter(Stats.uuid == item.uuid).update({Stats.last_date: None})
            session.commit()
        # date_in_datetime = datetime.fromisoformat(item_to_update.date.replace('Z', '+00:00'))
        if item_to_update.type == "OFFER":
            session.add(Stats(id=item_to_update.id,
                              name=item_to_update.name,
                              parentId=item_to_update.parentId,
                              type=item_to_update.type,
                              price=item_to_update.price,
                              date=item_to_update.date,
                              last_date=item_to_update.date,
                              ))
        elif item_to_update.type == "CATEGORY":
            check = session.query(Stats).filter(Stats.id == item_to_update.id, Stats.date == item_to_update.date).first()
            if check:
                check.price = item_to_update.price
                check.name = item_to_update.name
                check.parentId = item_to_update.parentId
                session.query(Stats).filter(Stats.uuid == check.uuid).update({
                    Stats.price: check.price,
                    Stats.name: check.name,
                    Stats.parentId: check.parentId,
                })
            else:
                session.add(Stats(id=item_to_update.id,
                                  name=item_to_update.name,
                                  parentId=item_to_update.parentId,
                                  type=item_to_update.type,
                                  price=item_to_update.price,
                                  date=item_to_update.date,
                                  last_date=item_to_update.date,
                                  ))
    return True


# when item_to_change updates and parentId doesn't change
def update_item_parentId_without_changes(session: Any, item_to_change: Item, found_item: Item,
                                         data: dict[str, Any]) -> bool:
    new_data_for_others = defaultdict(dict[str, Any])

    if item_to_change.type == "OFFER":
        new_data_for_others['price'] = item_to_change.price - found_item.price

        session.query(Item).filter(Item.id == item_to_change.id).update(data)
        update_statistics(session, item_to_change.id)

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
                    update_statistics(session, parent_item.id)
                elif parent_item.type == 'CATEGORY' and item_to_change.type == 'CATEGORY':

                    parent_item.all_price += new_data_for_others['price']

                    parent_item.date = data['date']

                    parent_item.price = parent_item.all_price // parent_item.count_items \
                        if parent_item.count_items else None

                    session.query(Item).filter(Item.id == parent_item.id).update(
                        dict(all_price=parent_item.all_price,
                             date=parent_item.date,
                             price=parent_item.price))
                    update_statistics(session, parent_item.id)
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
        update_statistics(session, item_to_change.id)
        # update all parents of this item_to_change
        while True:
            parent_item = session.query(Item).filter(Item.id == item_to_change.parentId).first()
            if parent_item:
                if parent_item.type == 'CATEGORY' and item_to_change.type == 'CATEGORY':
                    parent_item.date = data['date']
                    session.query(Item).filter(Item.id == parent_item.id).update(
                        dict(date=parent_item.date))
                    update_statistics(session, parent_item.id)
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
        found_item = found_item_original.copy()
        update_statistics(session, item_to_change.id)
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
                    update_statistics(session, parent_item.id)
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
                    update_statistics(session, parent_item.id)
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
        update_statistics(session, item_to_change.id)
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
                    update_statistics(session, parent_item.id)
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
                update_statistics(session, parent_item.id)
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
                    update_statistics(session, parent_item.id)
                    found_item = parent_item
            else:
                break

    session.query(Item).filter(Item.id == found_item_original.id).update(data)
    update_statistics(session, found_item_original.id)
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
                update_statistics(session, parent_item.id)
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
                    update_statistics(session, parent_item.id)
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

        update_statistics(session, item_to_add.id)

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
        update_statistics(session, item_to_add.id)
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
            update_statistics(session, parent_item.id)
            item_to_add = parent_item
        else:
            return True


def get_sales_from(item_date: datetime) -> list[Stats]:
    with create_session() as session:
        # date - 24 Hours
        date_from = item_date - timedelta(hours=24)
        # date_from to string
        date_from_str = date_from.strftime('%Y-%m-%dT%H:%M:%S')
        item_date_str = item_date.strftime('%Y-%m-%dT%H:%M:%S')
        logger.info('Getting sales from %s', date_from)
        logger.info('Getting sales to %s', item_date)
        items = session.query(Stats).filter(Stats.last_date is not None,
                                            Stats.last_date >= date_from_str,
                                            Stats.last_date <= item_date_str,
                                            Stats.type == "OFFER").all()
        logger.info('Got %s sales with items = %s', len(items), items)
        result_list = []
        for item in items:
            result_list.append(dict(
                id=item.id,
                name=item.name,
                parentId=item.parentId,
                type=item.type,
                price=item.price,
                date=item.last_date.isoformat()+'.000Z',
            ))
        logger.info('Got %s sales with items = %s', len(result_list), result_list)
        return result_list


def get_statistic_from(item_id: str, dateStart: datetime, dateEnd: datetime) -> list[Stats]:
    with create_session() as session:
        if not session.query(Item).filter(Item.id == item_id).first():
            return None
        dateStart = dateStart.strftime('%Y-%m-%dT%H:%M:%S')
        dateEnd = dateEnd.strftime('%Y-%m-%dT%H:%M:%S')
        logger.info('Getting statistic from %s', dateStart)
        logger.info('Getting statistic to %s', dateEnd)
        items = session.query(Stats).filter(Stats.id == item_id,
                                            Stats.date >= dateStart,
                                            Stats.date < dateEnd).all()
        logger.info('Got %s statistic with items = %s', len(items), items)
        result_list = []
        for item in items:
            result_list.append(dict(
                id=item.id,
                name=item.name,
                parentId=item.parentId,
                type=item.type,
                price=item.price,
                date=item.date.isoformat()+'.000Z',
            ))
        logger.info('Got %s statistic with items = %s', len(result_list), result_list)
        return result_list
