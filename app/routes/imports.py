import logging

from fastapi import APIRouter

from app.schemas import ShopUnitImportRequestSchema
from db.views import create_element

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix='/imports',
    tags=['Imports'],
    responses={
        200: {'description': 'Success'},
    },
)


@router.post('')
async def imports(data: ShopUnitImportRequestSchema) -> int:
    logger.info('DATA trnsmit started')
    logger.info('DATA RECEIEVED: %s', data)
    for item in data.items:
        logger.info('ITEM RECEIEVED: %s', item)
        create_element(date=data.updateDate, **item.dict())
    logger.info('DATA SAVED')
    return 200
