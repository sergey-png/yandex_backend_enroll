from db.models import Item


class ShopUnitView:
    def __init__(self, item: Item):
        self.id = item.id
        self.name = item.name
        self.date = item.date
        self.parentId = item.parentId
        self.type = item.type
        self.price = item.price
        self.children = [ShopUnitView(x) for x in item.children]
