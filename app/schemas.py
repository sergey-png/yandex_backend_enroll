from enum import Enum, unique
from typing import Any, Optional

from pydantic import BaseModel, validator


@unique
class ShopUnitType(str, Enum):
    OFFER = 'OFFER'
    CATEGORY = 'CATEGORY'


class ShopUnitSchema(BaseModel):
    id: str
    name: str
    date: str
    parentId: Optional[str]
    type: ShopUnitType
    price: Optional[int]
    children: Optional[list['ShopUnitSchema']]

    @validator('children', always=True)
    def validate_children(
        cls, value: Optional[list['ShopUnitSchema']], values: dict[str, Any]
    ) -> Optional[list['ShopUnitSchema']]:
        obj_type = values['type']

        if obj_type == ShopUnitType.OFFER:
            return None

        return value or []

    class Config:
        orm_mode = True


class ShopUnitImportSchema(BaseModel):
    id: str
    name: str
    parentId: Optional[str]
    type: ShopUnitType
    price: Optional[int]

    @validator('price', always=True)
    def validate_price(
        cls, value: Optional[int], values: dict[str, Any]
    ) -> Optional[int]:  # TODO
        return value


class ShopUnitImportRequestSchema(BaseModel):
    items: list[ShopUnitImportSchema]
    updateDate: str

    @validator('updateDate')
    def dvalidator_date(cls, value: str) -> str:  # TODO
        return value
