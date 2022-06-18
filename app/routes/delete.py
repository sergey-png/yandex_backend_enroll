import logging
from typing import Dict

from fastapi import APIRouter

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix='/delete',
    tags=['Delete'],
    responses={
        200: {'description': 'Success'},
        400: {'description': 'Validation Failed'},
        404: {'description': 'Item not found'},
    },
)


@router.delete('/{item_id}')
async def delete(item_id: str) -> Dict[str, str]:
    logger.info('DELETE %s', item_id)
    return {'id': item_id}
