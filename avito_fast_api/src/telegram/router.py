from fastapi import APIRouter, Request, Depends
from db import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from logger import logger
from .schemas import UpdateSchema
import json
from .services import send_message_to_avito


router = APIRouter(
    prefix="/api/v1/telegram",
    tags=["telegram"]
)

@router.post("/")
async def process_telegram_message(
        request: Request,
        session: AsyncSession = Depends(get_async_session)
):
    payload = await request.json()
    logger.info(json.dumps(payload))
    data = UpdateSchema(**payload)
    await send_message_to_avito(data, session)
    return {"ok": True}
