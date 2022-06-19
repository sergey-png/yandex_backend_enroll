import logging
from fastapi import HTTPException
from typing import Dict
from typing import Optional
import re

from fastapi import APIRouter


from db.views import get_one_element
from app.schemas import ShopUnitSchema


logger = logging.getLogger("uvicorn.error")

router = APIRouter(
    prefix='/nodes',
    tags=['Nodes'],
    responses={
        200: {'description': 'Success'},
        400: {'description': 'Validation Failed'},
        404: {'description': 'Item not found'},
    },
)


@router.get('/{item_id}', response_model=ShopUnitSchema)
async def get_nodes(item_id: str) -> Optional[list[ShopUnitSchema]]:
    logger.info('GET NODE WITH ID = %s', item_id)
    result = get_one_element(item_id)
    if result is None:
        raise HTTPException(status_code=404, detail='Item not found')
    return result
