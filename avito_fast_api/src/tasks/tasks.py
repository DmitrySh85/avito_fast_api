import asyncio

from celery import Celery
from celery.schedules import crontab

from settings import settings
from departments.services import get_department_ids
from reviews.manager import AvitoReviewManager


broker = settings.CELERY_BROKER

celery_app = Celery("tasks", broker=broker)
celery_app.autodiscover_tasks(["tasks"])


celery_app.conf.beat_schedule = {
    'celery_beat_testing': {
        'task': 'tasks.tasks.start_reviews',
        "schedule": crontab(hour="*/10")
    }
}


@celery_app.task
def start_reviews():
    asyncio.run(get_reviews())


async def get_reviews():
    department_ids = await get_department_ids()
    manager = AvitoReviewManager()
    for department_id in department_ids:
        await manager.get_reviews(department_id)
