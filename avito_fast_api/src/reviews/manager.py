from datetime import datetime

import requests
from sqlalchemy import select, func

from tokens.services import get_avito_token
from .schemas import AvitoReviewResponse, AvitoReview
from db import get_session
from logger import logger
from .models import Review
from notificator.telegram import TelegramNotificator
from departments.services import get_department_tg_group_id


class AvitoReviewManager:

    async def get_reviews(self, department_id: int):
        data = await self.send_review_request(department_id)
        if data.reviews:
            await self.insert_reviews(data.reviews, department_id)
            await self.send_reviews_to_tg(data.reviews, department_id)

    async def send_review_request(self, department_id: int) -> AvitoReviewResponse:
        url = "https://api.avito.ru/ratings/v1/reviews/"
        token = await self.get_authorization_token(department_id)
        headers = {"Authorization": f"Bearer {token}"}
        offset = await self.get_department_reviews_count(department_id)
        params = {
            "offset": offset,
            "limit": 20
        }
        try:
            response = requests.get(url=url, headers=headers, params=params)
        except Exception as e:
            logger.debug(e)
            return AvitoReviewResponse(total=0, reviews=list([]))
        data = response.json()
        logger.info(data)
        total = data.get("total", 0)
        reviews = data.get("reviews", list([]))
        return AvitoReviewResponse(
            total=total,
            reviews=[AvitoReview(**review) for review in reviews]
        )

    async def get_authorization_token(self, department_id: int) -> str:
        token = await get_avito_token(department_id)
        return token

    async def get_department_reviews_count(self, department_id: int) -> int:
        async with get_session() as session:
            stmt = select(func.count(Review.id)).filter(Review.department == department_id)
            result = await session.execute(stmt)
            return result.scalar()

    async def insert_reviews(
            self,
            reviews: list[AvitoReview],
            department_id: int
    ) -> None:
        reviews_to_save = [
            Review(
                id=review.id,
                score=review.score,
                stage=review.stage,
                text=review.text,
                used_in_score=review.usedInScore,
                can_answer=review.canAnswer,
                created_at=datetime.fromtimestamp(review.createdAt),
                department=department_id
            )
            for review in reviews
        ]
        async with get_session() as session:
            session.add_all(reviews_to_save)
            await session.commit()

    async def send_reviews_to_tg(
            self,
            reviews: list[AvitoReview],
            department_id: int,
    ):
        for review in reviews:
            await self.send_review_to_tg(review, department_id)

    async def send_review_to_tg(
            self,
            review: AvitoReview,
            department_id: int,
    ) -> None:
        notificator = TelegramNotificator()
        telegram_group_id = await get_department_tg_group_id(department_id)
        message_text = f"<b>Новый отзыв</b>\n{review.text}"
        topic = notificator.create_topic(telegram_group_id, review.text)
        response = notificator.send_message_to_topic(
            chat_id=telegram_group_id,
            text=message_text,
            message_thread_id=topic
            )
