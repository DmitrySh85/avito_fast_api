from fastapi import APIRouter, Request, Depends
from db import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from logger import logger
from .schemas import TelegramEventSchema
import json
from .services import send_message_to_avito


router = APIRouter(
    prefix="/api/v1/telegram",
    tags=["telegram"]
)

@router.post("/")
async def process_telegram_message(
        data: TelegramEventSchema,
        session: AsyncSession = Depends(get_async_session)
):

    await send_message_to_avito(data, session)
    return {"ok": True}
