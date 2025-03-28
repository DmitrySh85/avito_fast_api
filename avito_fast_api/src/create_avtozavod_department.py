import asyncio

from sqlalchemy import insert

from db import get_session
from departments.models import Department
from settings import settings


async def insert_department_to_db():
    department = {
            "address": 'Нижегородская обл., Нижний Новгород, ул. Юлиуса Фучика, 2А',
            "name": "Автозавод",
            "telegram_group_id": settings.DEPARTMENTS_GROUPS_IDS.get("Автозавод")
         }
    async with get_session() as session:
        stmt = insert(Department).values(**department)
        result = await session.execute(stmt)
        await session.commit()

if __name__ == "__main__":
    asyncio.run(insert_department_to_db())