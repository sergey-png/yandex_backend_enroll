import logging
from typing import Dict

from fastapi import APIRouter

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix='/delete',
    tags=['Delete'],
    responses={
        200: {'description': 'Success'},
    },
)


@router.delete('/{id}')
async def delete(item_id: int) -> Dict[str, int]:
    return {'id': item_id}
