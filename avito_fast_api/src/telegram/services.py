from fastapi import Depends
from requests import Response
from tokens.services import get_token
import requests
from db import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import TelegramEventSchema, SendMessageToAvitoSchema
from logger import logger
from settings import settings


async def send_message_to_avito(
        data: TelegramEventSchema,
        session: AsyncSession = Depends(get_async_session)
):
    avito_chat_id = data.chat_id
    avito_user_id = settings.AVITO_USER_ID
    logger.info(f"Received data: {data}")
    if not avito_chat_id or not avito_user_id:
        logger.debug("No avito_chat_id, avito_user_id")
    token = await get_token(session)
    if not token:
        return
    avito_message = SendMessageToAvitoSchema(
        token=token,
        chat_id=avito_chat_id,
        user_id=avito_user_id,
        text=data.text
    )
    response = send_api_message_to_avito(avito_message)
    logger.info(response)



def send_api_message_to_avito(
        message: SendMessageToAvitoSchema
) -> Response:
    url = f"https://api.avito.ru/messenger/v1/accounts/{message.user_id}/chats/{message.chat_id}/messages"
    headers = {"Authorization": f"Bearer {message.token}"}
    data = {
          "message": {
            "text": message.text
          },
          "type": "text"
}
    logger.info(SendMessageToAvitoSchema)
    response = requests.post(url=url, headers=headers, data=data)
    return response