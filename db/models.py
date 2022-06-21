from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BaseModel(Base):  # type: ignore
    __abstract__ = True

    uuid = sa.Column(
        sa.Integer,
        nullable=False,
        unique=True,
        primary_key=True,
        autoincrement=True,
    )
    created_at = sa.Column(
        sa.DateTime,
        nullable=False,
        default=datetime.now,
    )
    updated_at = sa.Column(
        sa.DateTime,
        nullable=False,
        default=datetime.now,
        onupdate=datetime.now,
    )

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}(uuid={self.uuid!r})>'


class Item(BaseModel):
    __tablename__ = 'item'

    id = sa.Column(sa.String, nullable=False, unique=True)
    name = sa.Column(sa.String, nullable=False)
    date = sa.Column(sa.String, nullable=False)
    type = sa.Column(sa.String, nullable=False)
    parentId = sa.Column(
        sa.ForeignKey('item.id', ondelete='CASCADE'), nullable=True
    )
    price = sa.Column(sa.Integer, nullable=True)
    all_price = sa.Column(sa.Integer, nullable=True)
    count_items = sa.Column(sa.Integer, nullable=True)

    children = sa.orm.relationship(
        'Item',
        backref=sa.orm.backref('parent', remote_side=[id]),
        cascade='all, delete-orphan',
        passive_deletes=True,
    )

    def copy(self, with_children=False):
        return Item(
            id=self.id,
            name=self.name,
            date=self.date,
            type=self.type,
            parentId=self.parentId,
            price=self.price,
            all_price=self.all_price,
            count_items=self.count_items,
            children=[child.copy() for child in self.children] if with_children else [],
        )
