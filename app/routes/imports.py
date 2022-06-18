import logging

from fastapi import APIRouter

from db.views import create_element
from app.schemas import ShopUnitImportRequestSchema

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix='/imports',
    tags=['imports'],
    responses={
        200: {'description': 'Success'},
    },
)


@router.post('')
async def imports(data: ShopUnitImportRequestSchema) -> int:
    for item in data.items:
        create_element(date=data.updateDate, **item.dict())
    return 200
