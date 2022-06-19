import logging
from fastapi import HTTPException
from typing import Dict
from typing import Optional
import re

from fastapi import APIRouter

from db.views import delete_element

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
async def delete(item_id: str) -> Optional[Dict[str, str]]:
    logger.info('DELETE %s', item_id)

    # check item_id format to be like "3fa85f64-5717-4562-b3fc-2c963f664338"
    r = re.compile('.{8}-.{4}-.{4}-.{4}-.{12}')
    if not r.match(item_id):
        logger.info('Item id %s is not valid', item_id)
        raise HTTPException(status_code=400, detail='Validation Failed')
    logger.info('Item id %s is valid', item_id)
    if delete_element(item_id):
        return {'id': item_id}
    else:
        raise HTTPException(status_code=404, detail='Item not found')
