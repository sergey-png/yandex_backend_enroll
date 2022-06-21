import logging
from datetime import datetime
from enum import Enum, unique
from typing import Any, Optional

from pydantic import BaseModel, validator

logger = logging.getLogger('uvicorn.error')


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
        logger.info('values = %s', values)
        logger.info('value = %s', value)
        obj_type = values.get('type')
        if obj_type is None:
            return None

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
    ) -> int:
        obj_type = values.get('type')
        if obj_type is None:
            raise ValueError('Type is required')
        if obj_type == ShopUnitType.CATEGORY and value is not None:
            raise ValueError(
                'Category price is not allowed for type "CATEGORY"'
            )
        if obj_type == ShopUnitType.OFFER and (value is None or value < 0):
            raise ValueError('Offer price must be greater than 0')
        return value


class ShopUnitImportRequestSchema(BaseModel):
    items: list[ShopUnitImportSchema]
    updateDate: str

    @validator('updateDate', always=True)
    def validate_date(cls, value: str) -> str:
        logger.info('Validating date: %s', value)
        try:
            dt_str = datetime.fromisoformat(value.replace('Z', '+00:00'))
            res_value = dt_str.isoformat().replace('+00:00', '.000Z')
            logger.info('No errors with validating: %s', res_value)
            return res_value
        except (ValueError, TypeError) as exc:
            logger.info('Error with validating: %s', value)
            raise ValueError('Invalid date format') from exc

    @validator('items', always=True)
    def validate_items(
        cls, value: list[ShopUnitImportSchema]
    ) -> list[ShopUnitImportSchema]:
        logger.info('**************Validating items: %s', value)
        result_items: set = set()
        for item in value:
            logger.info('Validating item: %s', item)
            result_items.add(item.id)
        if len(result_items) != len(value):
            raise ValueError('Duplicate items')
        return value
