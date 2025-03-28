import pytest

from departments.services import get_department_ids
from reviews.manager import AvitoReviewManager


@pytest.mark.asyncio
async def test_fetch_reviews_success():
    department_ids = await get_department_ids()
    manager = AvitoReviewManager()
    for department_id in department_ids:
        await manager.get_reviews(department_id)