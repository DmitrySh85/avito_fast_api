from datetime import datetime, timedelta

import requests
from settings import settings
from logger import logger
from db import get_async_session
from fastapi import Depends
from sqlalchemy import select, update, delete, insert
from sqlalchemy.ext.asyncio import AsyncSession
from .models import AccessToken


def get_access_token() -> str | None:
    url = 'https://api.avito.ru/token/'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = {
        'grant_type': 'client_credentials',
        'client_id': settings.CLIENT_ID,
        'client_secret': settings.CLIENT_SECRET
    }

    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 200:
        response_data = response.json()
    else:
        logger.debug(f'Error fetching token:{response.status_code}, {response.text}')
        return
    access_token = response_data.get("access_token")
    if not access_token:
        logger.debug(f"Error fetching token: {response_data}")
    return access_token


async def get_token(
        session: AsyncSession = Depends(get_async_session)
) -> str | None:
    logger.info("Fetching token from db")
    token = await get_token_from_db(session)
    if not token:
        logger.info("No token in db or token is expired. Fetching token by API.")
        token = get_access_token()
        await refresh_token_in_db(token, session)
    return token


async def get_token_from_db(
        session: AsyncSession = Depends(get_async_session)
) -> str | None:
    current_time = datetime.now()
    stmt = select(AccessToken.token).where(AccessToken.expires_at > current_time)
    result = await session.execute(stmt)
    return result.fetchone().token


async def refresh_token_in_db(
        token: str,
        session: AsyncSession = Depends(get_async_session)
) -> None:
    stmt = delete(AccessToken)
    await session.execute(stmt)
    await session.commit()

    expires_at = datetime.now() + timedelta(hours=24)
    stmt = insert(AccessToken).values(
        token=token, expires_at=expires_at
    )
    await session.execute(stmt)
    await session.commit()