import logging
from typing import Dict, Optional

from fastapi import APIRouter, HTTPException

from db.views import delete_element

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix='/delete',
    tags=['Delete'],
    responses={
        200: {'description': 'Success'},
        400: {'description': 'Validation Failed'},
    },
)


@router.delete('/{item_id}')
async def delete(item_id: str) -> Optional[Dict[str, str]]:
    logger.info('DELETE %s', item_id)

    if delete_element(item_id):
        return {'id': item_id}
    else:
        raise HTTPException(status_code=404, detail='Item not found')
