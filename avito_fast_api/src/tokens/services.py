from datetime import datetime, timedelta

import requests
from settings import settings
from logger import logger
from db import get_async_session, get_session
from fastapi import Depends
from sqlalchemy import select, update, delete, insert
from sqlalchemy.ext.asyncio import AsyncSession
from .models import AccessToken
from departments.models import Department



async def get_access_token(department_id: int) -> str | None:
    url = 'https://api.avito.ru/token/'
    department_name = await get_department(department_id)
    try:
        department = list(filter(lambda x: x.get("name") == department_name, settings.DEPARTMENTS_CLIENT_SECRETS))[0]
    except KeyError:
        department = {}
    client_id = department.get("client_id")
    client_secret = department.get("client_secret")
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret
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


async def get_department(department_id: int) -> str | None:
    async with get_session() as session:
        stmt = select(Department.name).where(Department.id == department_id)
        result = await session.execute(stmt)
        return result.scalar()


async def get_token(
        department_id: int,
        session: AsyncSession = Depends(get_async_session)
) -> str | None:
    logger.info("Fetching token from db")
    token = await get_token_from_db(department_id, session)
    if not token:
        logger.info("No token in db or token is expired. Fetching token by API.")
        token = await get_access_token(department_id)
        await refresh_token_in_db(token, department_id, session)
    return token


async def get_token_from_db(
        department_id: int,
        session: AsyncSession = Depends(get_async_session)
) -> str | None:
    current_time = datetime.now()
    stmt = select(AccessToken.token).where(
        AccessToken.department_id == department_id,
        AccessToken.expires_at > current_time
    )
    result = await session.execute(stmt)
    try:
        return result.fetchone().token
    except AttributeError:
        return


async def refresh_token_in_db(
        token: str,
        department_id: int,
        session: AsyncSession = Depends(get_async_session)
) -> None:
    stmt = delete(AccessToken).where(AccessToken.department_id == department_id)
    await session.execute(stmt)
    await session.commit()

    expires_at = datetime.now() + timedelta(hours=24)
    stmt = insert(AccessToken).values(
        token=token, expires_at=expires_at, department_id=department_id
    )
    await session.execute(stmt)
    await session.commit()