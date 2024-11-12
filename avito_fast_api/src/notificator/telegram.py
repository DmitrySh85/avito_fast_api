from settings import settings
import requests
from logger import logger
from db import get_async_session
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from message.models import Chat


class TelegramNotificator:
    def __init__(self):
        self.bot_token = settings.BOT_TOKEN

    def send_message(self, chat_id, message):
        return requests.post(
            f"https://api.telegram.org/bot{self.bot_token}/sendMessage",
            data={"chat_id": chat_id, "text": message, "parse_mode": "Markdown"},
        )

    async def get_topic(
            self,
            chat_id: str,
            session: AsyncSession = Depends(get_async_session)
    ):
        stmt = select(Chat.telegram_topic).where(Chat.id == chat_id)
        result = await session.execute(stmt)
        return result.scalar()

    def create_topic(
            self,
            group_id: int,
            name: str
    ):
        url = f'https://api.telegram.org/bot{self.bot_token}/createForumTopic'
        payload = {
            "chat_id": group_id,
            "name": name
        }
        response = requests.post(url=url, json=payload)
        return response.json()

    def send_message_to_topic(
            self,
            chat_id: int,
            text: str,
            message_thread_id: str
    ):
        return requests.post(
            f"https://api.telegram.org/bot{self.bot_token}/sendMessage",
            data={
                "chat_id": chat_id,
                "text": text,
                "message_thread_id": message_thread_id,
                "parse_mode": "HTML"},
        )