import logging
from datetime import datetime
from typing import Any, Optional

from fastapi import APIRouter, HTTPException

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
async def get_sales(date: str) -> dict[str, Any]:
    date2 = validate_date(date)
    logger.info('date is %s', date2)
    if date2 is None:
        raise HTTPException(status_code=400, detail='Validation Failed')
    return {'items': get_sales_from(date2)}


def validate_date(value: str) -> Optional[datetime]:
    try:
        res_value = datetime.fromisoformat(value.replace('Z', '+00:00'))
        # res_value = dt_str.isoformat().replace('+00:00', '.000Z')
        logger.info('No errors with validating: %s', res_value)
        return res_value
    except (ValueError, TypeError) as exc:
        logger.info('Error with validating: %s', exc)
        return None
