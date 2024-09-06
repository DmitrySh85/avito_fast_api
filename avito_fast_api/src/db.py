from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy import NullPool, MetaData
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)
from sqlalchemy.ext.declarative import declarative_base

from settings import settings

Base = declarative_base()
engine = create_async_engine(settings.db_url, poolclass=NullPool)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


@asynccontextmanager
async def get_session():
    try:
        async_session = async_sessionmaker(engine)
        async with async_session() as session:
            yield session
    except:
        await session.rollback()
        raise
    finally:
        await session.close()