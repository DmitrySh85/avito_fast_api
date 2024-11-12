from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from db import get_async_session
from message.models import Chat
from departments.models import Department


async def get_chat_id_from_db(
        telegram_chat_id: int,
        message_thread_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    stmt = select(Chat.id).join(
        Department, Chat.department_id == Department.id
    ).where(
        Department.telegram_group_id == telegram_chat_id,
        Chat.telegram_topic == message_thread_id
    )
    result = await session.execute(stmt)
    return result.scalar()