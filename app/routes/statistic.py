import logging
from typing import Optional, Any

from datetime import datetime
from fastapi import APIRouter, HTTPException

from app.schemas import ShopUnitStatisticUnitSchema
from app.schemas import ShopUnitStatisticResponseSchema

from db.views import get_sales_from
from db.views import get_statistic_from

logger = logging.getLogger('uvicorn.error')

router = APIRouter(
    prefix='/node',
    tags=['Statistic'],
    responses={
        200: {'description': 'Success'},
        400: {'description': 'Validation Failed'},
        404: {'description': 'Item not found'},
    },
)


@router.get('/{item_id}/statistic', response_model=ShopUnitStatisticResponseSchema)
async def get_statistic(item_id: str, dateStart: str, dateEnd: str) -> ShopUnitStatisticResponseSchema:
    dateStart = validate_date(dateStart)
    dateEnd = validate_date(dateEnd)
    if dateStart is None or dateEnd is None:
        raise HTTPException(status_code=400, detail='Validation Failed')
    result = get_statistic_from(item_id, dateStart, dateEnd)
    if result is None:
        raise HTTPException(status_code=404, detail='Item not found')
    return {'items': result}


def validate_date(value: str) -> Optional[datetime]:
    try:
        res_value = datetime.fromisoformat(value.replace('Z', '+00:00'))
        # res_value = dt_str.isoformat().replace('+00:00', '.000Z')
        logger.info('No errors with validating: %s', res_value)
        return res_value
    except (ValueError, TypeError) as exc:
        logger.info('Error with validating: %s', value)
        return None
