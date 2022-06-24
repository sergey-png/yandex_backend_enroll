import logging
from typing import Optional

from datetime import datetime
from fastapi import APIRouter, HTTPException

from app.schemas import ShopUnitStatisticUnitSchema
from app.schemas import ShopUnitStatisticResponseSchema

from db.views import get_sales_from

logger = logging.getLogger('uvicorn.error')

router = APIRouter(
    prefix='/sales',
    tags=['Sales'],
    responses={
        200: {'description': 'Success'},
        400: {'description': 'Validation Failed'},
    },
)


@router.get('', response_model=ShopUnitStatisticResponseSchema)
async def get_sales(date: str) -> ShopUnitStatisticResponseSchema:
    date = validate_date(date)
    logger.info("date is %s", date)
    if date is None:
        raise HTTPException(status_code=400, detail='Validation Failed')
    return {'items': get_sales_from(date)}


def validate_date(value: str) -> Optional[datetime]:
    try:
        res_value = datetime.fromisoformat(value.replace('Z', '+00:00'))
        # res_value = dt_str.isoformat().replace('+00:00', '.000Z')
        logger.info('No errors with validating: %s', res_value)
        return res_value
    except (ValueError, TypeError) as exc:
        logger.info('Error with validating: %s', value)
        return None
