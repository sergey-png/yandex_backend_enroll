import logging
from datetime import datetime
from enum import Enum, unique
from typing import Any, Optional

from pydantic import BaseModel, validator

logger = logging.getLogger(__name__)


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
    ) -> Optional[int]:  # TODO write new validator
        return value


class ShopUnitImportRequestSchema(BaseModel):
    items: list[ShopUnitImportSchema]
    updateDate: str

    @validator('updateDate', always=True)
    def validate_date(cls, value: str) -> Optional[str]:
        print(f'Validating date: {value}')
        logger.info('Validating date: %s', value)
        try:
            dt_str = datetime.fromisoformat(value.replace('Z', '+00:00'))
            res_value = dt_str.isoformat().replace('+00:00', '.000Z')
            logger.info('No errors with validating: %s', res_value)
            return res_value
        except (ValueError, TypeError):
            logger.info('Error with validating: %s', value)
            return ValueError('Invalid date format')
