from fastapi import APIRouter, Request, Depends
from logger import logger
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import AvitoMessageSchema
import json
from .services import process_avito_message
from db import get_async_session


router = APIRouter(
    prefix="/api/v1/webhook",
    tags=["avito"]
)

@router.post("/")
async def receive_webhook(
        request: Request,
        session: AsyncSession = Depends(get_async_session)
):
    payload = await request.json()
    logger.info(json.dumps(payload))
    data = AvitoMessageSchema(**payload)
    await process_avito_message(data, session)
    return {"ok": True}