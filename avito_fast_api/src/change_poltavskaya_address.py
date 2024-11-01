import asyncio

from sqlalchemy import update

from db import get_session
from departments.models import Department


async def change_department_address():
    async with get_session() as session:
        stmt = update(Department).values(
            {"address": "Нижегородская обл., Нижний Новгород, Полтавская ул., 30к2"}
        ).where(Department.name == "Полтавская")
        await session.execute(stmt)
        await session.commit()


if __name__ == "__main__":
    asyncio.run(change_department_address())