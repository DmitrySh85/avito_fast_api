from fastapi import APIRouter, Depends, Query
from db import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from .services import get_chat_id_from_db
from logger import logger


router = APIRouter(
    prefix="/api/v1/chat",
    tags=["chat"]
)


@router.get("/")
async def get_chat_id(
        telegram_chat_id: int = Query(None),
        message_thread_id: int = Query(None),
        session: AsyncSession = Depends(get_async_session)
):

    chat_id = await get_chat_id_from_db(telegram_chat_id, message_thread_id, session)
    return {"chat_id": chat_id}

