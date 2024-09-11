from fastapi import Depends
from requests import Response
from tokens.services import get_token

from db import get_async_session
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import UpdateSchema, SendMessageToAvitoSchema
from message.models import (
    AvitoMessage,
    Content,
    Location,
    Image,
    Call,
    Link,
    Item,
)
from logger import logger
import requests


async def send_message_to_avito(
        data: UpdateSchema,
        session: AsyncSession = Depends(get_async_session)
):
    avito_chat_id, avito_user_id = await get_avito_chat_data(data, session)
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
        text=data.message.text
    )
    response = send_api_message_to_avito(avito_message)
    logger.info(response)


async def get_avito_chat_data(
        data: UpdateSchema,
        session: AsyncSession = Depends(get_async_session)
):
    message_id = data.message.reply_to_message.message_id
    if data.message.reply_to_message.location:
        try:
            avito_chat_id, avito_user_id = await get_avito_chat_data_from_location(message_id, session)
        except TypeError:
            logger.debug("No chat id found")
            avito_chat_id, avito_user_id = None, None

    elif data.message.reply_to_message.photo:
        try:
            avito_chat_id, avito_user_id = await get_avito_chat_data_from_photo(message_id, session)
            print(avito_chat_id, avito_user_id)
        except TypeError:
            logger.debug("No chat id found")
            avito_chat_id, avito_user_id = None, None
    else:
        try:
            avito_chat_id, avito_user_id = await get_avito_chat_data_from_text_fields(message_id, session)
        except TypeError:
            logger.debug("No chat id found")
            avito_chat_id, avito_user_id = None, None
    return avito_chat_id, avito_user_id


async def get_avito_chat_data_from_location(
        message_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    stmt = select(
        AvitoMessage.chat_id, AvitoMessage.user_id
    ).join(Content, Content.id == AvitoMessage.content_id).join(
        Location, Location.id == Content.location_id
    ).where(Location.tg_message_id == message_id)
    result = await session.execute(stmt)
    return result.fetchone()


async def get_avito_chat_data_from_photo(
        message_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    stmt = select(
        AvitoMessage.chat_id, AvitoMessage.user_id
    ).join(Content, Content.id == AvitoMessage.content_id).join(
        Image, Image.id == Content.image_id
    ).where(Location.tg_message_id == message_id)
    result = await session.execute(stmt)
    return result.fetchone()


async def get_avito_chat_data_from_text_fields(
        message_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    result = await get_avito_chat_data_from_call(message_id, session)
    if result:
        return result
    result = await get_avito_chat_data_from_link(message_id, session)
    if result:
        return result
    result = await get_avito_chat_data_from_item(message_id, session)
    if result:
        return result
    result = await get_avito_chat_data_from_content(message_id, session)
    if result:
        return result


async def get_avito_chat_data_from_call(
        message_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    stmt = select(
        AvitoMessage.chat_id, AvitoMessage.user_id
    ).join(Content, Content.id == AvitoMessage.content_id).join(
        Call, Call.id == Content.call_id
    ).where(Call.tg_message_id == message_id)
    result = await session.execute(stmt)
    return result.fetchone()


async def get_avito_chat_data_from_link(
        message_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    stmt = select(
        AvitoMessage.chat_id, AvitoMessage.user_id
    ).join(Content, Content.id == AvitoMessage.content_id).join(
        Link, Link.id == Content.link_id
    ).where(Link.tg_message_id == message_id)
    result = await session.execute(stmt)
    return result.fetchone()


async def get_avito_chat_data_from_item(
        message_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    stmt = select(
        AvitoMessage.chat_id, AvitoMessage.user_id
    ).join(Content, Content.id == AvitoMessage.content_id).join(
        Item, Item.id == Content.item_id
    ).where(Item.tg_message_id == message_id)
    result = await session.execute(stmt)
    return result.fetchone()


async def get_avito_chat_data_from_content(
        message_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    stmt = select(
        AvitoMessage.chat_id, AvitoMessage.user_id
    ).join(Content, Content.id == AvitoMessage.content_id
           ).where(Content.tg_message_id == message_id)
    result = await session.execute(stmt)
    return result.fetchone()


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
    response = requests.post(url=url, headers=headers, data=data)
    return response