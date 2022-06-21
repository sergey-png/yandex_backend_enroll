import logging

from fastapi import APIRouter, HTTPException

from app.schemas import ShopUnitImportRequestSchema
from db.views import create_element

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix='/imports',
    tags=['Imports'],
    responses={
        200: {'description': 'Success'},
        400: {'description': 'Validation Failed'},
    },
)


@router.post('')
async def imports(data: ShopUnitImportRequestSchema) -> int:
    logger.info('DATA trnsmit started')
    logger.info('DATA RECEIEVED: %s', data)

    logger.info('No duplicate items found')
    for item in data.items:
        logger.info('ITEM RECEIEVED: %s', item)
        if create_element(date=data.updateDate, **item.dict()):
            logger.info('ITEM CREATED: %s', item)
        else:
            logger.info('ITEM NOT CREATED: %s', item)
            raise HTTPException(status_code=400, detail='Validation Failed')
    logger.info('DATA SAVED')
    return 200
