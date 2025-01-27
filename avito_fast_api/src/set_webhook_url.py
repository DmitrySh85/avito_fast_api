from typing import List

import requests
from sqlalchemy import select

from tokens.services import get_access_token
from settings import settings
from logger import logger
import asyncio
from departments.models import Department
from db import get_session


async def set_webhook_url():
    departments = await get_departments()
    for department in departments:
        if department.name == "Лианозово":
            continue
        department_id = department.id
        logger.info(f"Setting webhook: {settings.WEBHOOK_URL}/{department_id}/")
        url = "https://api.avito.ru/messenger/v3/webhook"
        access_token = await get_access_token(department_id)

        headers = {"Authorization": f"Bearer {access_token}"}
        data = {
            "url": f"{settings.WEBHOOK_URL}{department_id}/"
        }
        print(department.id, department.name, access_token, data)
        response = requests.post(url, headers=headers, json=data)
        print(response)
        if response.status_code == 200:
            logger.info(response.json())
        else:
            logger.info(response.content)
        await asyncio.sleep(10)


async def get_departments() -> List[Department]:
    async with get_session() as session:
        stmt = select(Department)
        result = await session.execute(stmt)
        return result.scalars().all()


if __name__ == "__main__":
    asyncio.run(set_webhook_url())