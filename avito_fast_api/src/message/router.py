from fastapi import APIRouter, Request, Depends
from logger import logger
from pydantic_core import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import Object
import json
from .services import process_avito_message
from db import get_async_session
from settings import settings


router = APIRouter(
    prefix="/api/v1/webhook",
    tags=["avito"]
)

"""
@router.post("/")
async def receive_webhook(
        request: Request,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        payload = await request.json()
        logger.info(json.dumps(payload))
        data = Object(**payload)
        await process_avito_message(data.payload.value, session)
    except ValidationError as e:
        logger.debug(e)
    #except Exception as exception:
    #    logger.info(exception)
    #finally:
    return {"ok": True}
"""

@router.post("/{department_id}/")
async def process_webhook(
        department_id: int,
        request: Request,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        payload = await request.json()
        logger.info(json.dumps(payload))
        logger.info(f"{department_id=}")
        data = Object(**payload)
        await process_avito_message(data.payload.value, department_id, session)
    except ValidationError as e:
        logger.debug(f"Catch integrity error: {e}")
    return {"ok": True}
