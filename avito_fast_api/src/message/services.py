from fastapi import Depends
from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import (
    AvitoMessageSchema,
    CreateContentSchema,
    CallSchema,
    CreateAvitoMessageSchema,
)
from .models import (
    Call,
    Content,
    Chat,
    AvitoMessage
)
from notificator.telegram import TelegramNotificator
from static_text.static_text import RECEIVED_AVITO_CALL
from requests.models import Response
from logger import logger
from db import get_async_session
from items.manager import AvitoItemManager
from departments.services import (
    get_department_group_id,
    get_department_id
)
from settings import settings


async def process_avito_message(
        data: AvitoMessageSchema,
        department_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    message_is_incoming = data.author_id != data.user_id
    if message_is_incoming and data.type != "system":
        logger.info(f"INCOMING MESSAGE {message_is_incoming}")
        message_in_db = await check_message_in_db(data, session)
        logger.info(f"DB SAYS: {message_in_db}")
        if message_in_db:
            logger.info("Message is already in db")
            return
        sent_to_tg_data = await send_avito_message_to_tg(data, department_id, session)
        try:
            await insert_avito_message_to_db(sent_to_tg_data, session)
        except IntegrityError as e:
            logger.debug(e)


async def check_message_in_db(
        data: AvitoMessageSchema,
        session: AsyncSession = Depends(get_async_session)
):
    logger.info(data)
    stmt = select(AvitoMessage.id).where(
        AvitoMessage.id == data.id,
    )
    result = await session.execute(stmt)
    return result.fetchall()


async def send_avito_message_to_tg(
        data: AvitoMessageSchema,
        department_id: int,
        session: AsyncSession = Depends(get_async_session)
) -> AvitoMessageSchema:
    telegram = TelegramNotificator()

    content = data.content

    item_id = data.item_id
    items_manager = AvitoItemManager(session)
    item = await items_manager.get_item_from_avito(item_id, department_id)
    department = item.get("address")
    department_group_id = await get_department_group_id(department, session)
    data.department_id = department_id
    logger.debug(f"Fetched department_group_id from DB: {department_group_id}")

    if department_group_id is None:
        department_group_id = settings.ADMIN_TG_ID
        logger.debug(f"Get group chat from .env: {department_group_id}")

    title = item.get("title")

    if content.text:
        message_thread_id = await telegram.get_topic(data.chat_id, session)
        if not message_thread_id:
            topic = telegram.create_topic(department_group_id, data.chat_id)
            message_thread_id = topic.get("result", {}).get('message_thread_id')
            text = f"Сообщение по объявлению: \n<b>{title}</b>\n{content.text}"
        else:
            text = content.text
        data.telegram_topic = message_thread_id
        response = telegram.send_message_to_topic(
            chat_id=department_group_id, 
            text=text,
            message_thread_id=message_thread_id
            )
        logger.info(response.json())
        content.tg_message_id = get_telegram_message_id(response)

    if content.call:
        text = RECEIVED_AVITO_CALL.format(
            target_user_id=content.call.target_user_id,
            status=content.call.status,
            title=title,
            department=department)
        message_thread_id = await telegram.get_topic(data.chat_id, session)
        if not message_thread_id:
            topic = telegram.create_topic(department_group_id, data.chat_id)
            message_thread_id = topic.get("result", {}).get('message_thread_id')
        data.telegram_topic = message_thread_id
        response = telegram.send_message_to_topic(
            chat_id=department_group_id,
            text=text,
            message_thread_id=message_thread_id
        )
        logger.info(response.json())
        content.tg_message_id = get_telegram_message_id(response)

    return data


def get_telegram_message_id(response: Response) -> int | None:
    if response.status_code == 200:
        response_data = response.json()
        tg_message_id = response_data["result"]["message_id"]
        return tg_message_id
    logger.debug(f"Returned {response=}")
    return None


async def insert_avito_message_to_db(
        data: AvitoMessageSchema,
        session: AsyncSession = Depends(get_async_session)
):
    content = CreateContentSchema(
        text=data.content.text,
        tg_message_id=data.content.tg_message_id
    )
    if data.content.call:
        content.call_id = await insert_call_to_db(data.content.call, session)

    content_id = await insert_content_to_db(content, session)
    chat_id = await insert_chat_to_db(data, session)
    avito_message = CreateAvitoMessageSchema(
        content_id=content_id,
        author_id=data.author_id,
        chat_id=chat_id,
        created=data.created,
        id=data.id,
        item_id=data.item_id,
        read=data.read,
        type=data.type,
        user_id=data.user_id,
        created_at=data.published_at
    )
    await insert_message_to_db(avito_message, session)


async def insert_call_to_db(
        call: CallSchema,
        session: AsyncSession = Depends(get_async_session)
) -> int:
    new_call = Call(**call.model_dump())
    session.add(new_call)
    await session.commit()
    await session.refresh(new_call)
    return new_call.id


async def insert_content_to_db(
        content: CreateContentSchema,
        session: AsyncSession = Depends(get_async_session)
) -> int:
    new_content = Content(**content.model_dump())
    session.add(new_content)
    await session.commit()
    await session.refresh(new_content)
    return new_content.id


async def insert_chat_to_db(
        data: AvitoMessageSchema,
        session: AsyncSession = Depends(get_async_session)
) -> str:
    await session.merge(
        Chat(
            id=data.chat_id,
            chat_type=data.chat_type,
            telegram_topic=data.telegram_topic,
            department_id=data.department_id
        ))
    await session.commit()
    return data.chat_id


async def insert_message_to_db(
        message: CreateAvitoMessageSchema,
        session: AsyncSession = Depends(get_async_session)
):
    message_data = message.model_dump()
    message_data.pop('telegram_topic', None)
    new_message = AvitoMessage(**message_data)
    session.add(new_message)
    await session.commit()
