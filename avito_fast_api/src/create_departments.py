import asyncio

from sqlalchemy import insert

from db import get_session
from departments.models import Department
from settings import settings


async def insert_departments_to_db():
    departments = [
        {
            "address": "Москва, Лианозовский пр., 14с1",
            "name": "Лианозово",
            "telegram_group_id": settings.DEPARTMENTS_GROUPS_IDS.get("Лианозово")
         },
        {
            "address": "Нижегородская обл., Нижний Новгород, ул. Федосеенко, 69А",
            "name": "Федосеенко",
            "telegram_group_id": settings.DEPARTMENTS_GROUPS_IDS.get("Федосеенко")
        },
        {
            "address": "Нижегородская обл., Нижний Новгород, Полтавская ул., 30к2",
            "name": "Полтавская",
            "telegram_group_id": settings.DEPARTMENTS_GROUPS_IDS.get("Полтавская")
        },
        {
            "address": 'Нижегородская обл., Нижний Новгород, ул. Юлиуса Фучика, 2А',
            "name": "Автозавод",
            "telegram_group_id": settings.DEPARTMENTS_GROUPS_IDS.get("Автозавод")
        }
    ]

    async with get_session() as session:
        stmt = insert(Department)
        result = await session.execute(stmt, departments)
        await session.commit()

if __name__ == "__main__":
    asyncio.run(insert_departments_to_db())