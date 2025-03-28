from fastapi import Depends
from requests import Response, JSONDecodeError
from sqlalchemy import select
from tokens.services import get_token
import requests
from db import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import TelegramEventSchema, SendMessageToAvitoSchema
from logger import logger
from settings import settings
from message.models import AvitoMessage, Chat
from reviews.manager import AvitoReviewManager


async def send_message_to_avito(
        data: TelegramEventSchema,
        session: AsyncSession = Depends(get_async_session)
) -> None:
    avito_chat_id = data.chat_id
    if not avito_chat_id.startswith("u2i"):
        review_manager = AvitoReviewManager()
        await review_manager.send_reply_to_review(data)
        return

    department_id = await get_department_id_from_chat(avito_chat_id, session)
    avito_user_id = await get_user_id(avito_chat_id, session)
    logger.info(f"{avito_user_id=}")
    logger.info(f"Received data: {data}")

    if not avito_chat_id or not avito_user_id or not department_id:
        logger.debug("No avito_chat_id, avito_user_id, department_id")
        return
    token = await get_token(department_id, session)
    if not token:
        return
    avito_message = SendMessageToAvitoSchema(
        token=token,
        chat_id=avito_chat_id,
        user_id=avito_user_id,
        text=data.text
    )
    response = send_api_message_to_avito(avito_message)
    if response.status_code == 200:
        logger.info("Message has been sent to avito")


def send_api_message_to_avito(
        message: SendMessageToAvitoSchema
) -> Response:
    url = f"https://api.avito.ru/messenger/v1/accounts/{message.user_id}/chats/{message.chat_id}/messages/"
    headers = {"Authorization": f"Bearer {message.token}"}
    data = {
          "message": {
            "text": message.text
          },
          "type": "text"
}
    logger.info(SendMessageToAvitoSchema)
    response = requests.post(url=url, headers=headers, json=data)
    return response


async def get_user_id(
        avito_chat_id: str,
        session: AsyncSession = Depends(get_async_session)
) -> int | None:
    stmt = select(AvitoMessage.user_id
                  ).join(Chat, AvitoMessage.chat_id == Chat.id
                         ).where(Chat.id == avito_chat_id)
    result = await session.execute(stmt)
    return result.scalar()


async def get_department_id_from_chat(
        avito_chat_id: str,
        session
) -> int | None:
    stmt = select(Chat.department_id).where(Chat.id == avito_chat_id)
    result = await session.execute(stmt)
    return result.scalar()
