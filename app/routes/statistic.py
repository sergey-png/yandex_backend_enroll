import logging
from typing import Any

from fastapi import APIRouter, HTTPException

from app.routes.sales import validate_date
from app.schemas import ShopUnitStatisticResponseSchema
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


@router.get(
    '/{item_id}/statistic', response_model=ShopUnitStatisticResponseSchema
)
async def get_statistic(item_id: str, dateStart: str, dateEnd: str) -> Any:
    dateStart2 = validate_date(dateStart)
    dateEnd2 = validate_date(dateEnd)
    if dateStart2 is None or dateEnd2 is None:
        raise HTTPException(status_code=400, detail='Validation Failed')
    result = get_statistic_from(item_id, dateStart2, dateEnd2)
    if result is None:
        raise HTTPException(status_code=404, detail='Item not found')
    return {'items': result}
