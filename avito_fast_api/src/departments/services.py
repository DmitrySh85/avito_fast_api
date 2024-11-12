from db import get_async_session
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .models import Department


async def get_department_chat_id(
        address: str,
        session: AsyncSession = Depends(get_async_session)
):
    stmt = select(Department.telegram_channel_id).where(Department.address == address)
    result = await session.execute(stmt)
    return result.scalar()


async def get_department_group_id(
        address: str,
        session: AsyncSession = Depends(get_async_session)
):
    stmt = select(Department.telegram_group_id).where(Department.address == address)
    result = await session.execute(stmt)
    return result.scalar()


async def get_department_id(
    address: str,
    session: AsyncSession = Depends(get_async_session)
):
    stmt = select(Department.id).where(Department.address == address)
    result = await session.execute(stmt)
    return result.scalar()