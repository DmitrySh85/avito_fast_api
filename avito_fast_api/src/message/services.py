from fastapi import Depends
from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import (
    AvitoMessageSchema,
    ImageSchema,
    LocationSchema,
    LinkSchema,
    ItemSchema,
    LinkPreviewSchema,
    CreateContentSchema,
    CallSchema,
    CreateAvitoMessageSchema,
)
from .models import (
    Location,
    Link,
    LinkPreview,
    Item,
    Image,
    Call,
    Content,
    Chat,
    AvitoMessage
)
from notificator.telegram import TelegramNotificator
from settings import settings
from static_text.static_text import MESSAGE_RECEIVED, RECEIVED_AVITO_CALL
from requests.models import Response
from logger import logger
from db import get_async_session
from items.manager import AvitoItemManager


async def process_avito_message(
        data: AvitoMessageSchema,
        session: AsyncSession = Depends(get_async_session)
):
    message_is_incoming = data.author_id != data.user_id
    if message_is_incoming:
        logger.info(f"INCOMING MESSAGE {message_is_incoming}")
        message_in_db = await check_message_in_db(data, session)
        logger.info(f"DB SAYS: {message_in_db}")
        if message_in_db:
            logger.info("Message is already in db")
            return
        sent_to_tg_data = await send_avito_message_to_tg(data, session)
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
        session: AsyncSession = Depends(get_async_session)
) -> AvitoMessageSchema:
    telegram = TelegramNotificator()

    content = data.content

    item_id = data.item_id
    logger.info(f"item_id: {item_id}")
    items_manager = AvitoItemManager(session)
    item = await items_manager.get_item_from_avito(item_id)
    department = item.get("address")
    title = item.get("title")

    telegram.send_message(
        settings.ADMIN_TG_ID,
        MESSAGE_RECEIVED.format(department=department, title=title))

    if content.text:
        response = telegram.send_message(settings.ADMIN_TG_ID, content.text)
        content.tg_message_id = get_telegram_message_id(response)

    if content.call:
        text = RECEIVED_AVITO_CALL.format(
            target_user_id=content.call.target_user_id,
            status=content.call.status
        )
        response = telegram.send_message(settings.ADMIN_TG_ID, text)
        content.call.tg_message_id = get_telegram_message_id(response)

    if data.content.image:
        max_image_link = get_max_image_link(content.image)
        response = telegram.send_picture(settings.ADMIN_TG_ID, max_image_link)
        content.image.tg_message_id = get_telegram_message_id(response)

    if content.item:
        caption = f"{content.item.title} {content.item.price_string} {content.item.item_url}".strip()
        response = telegram.send_picture(settings.ADMIN_TG_ID, content.item.image_url, caption)
        content.item.tg_message_id = get_telegram_message_id(response)

    if content.link:
        text = f"{content.link.text} {content.link.url}"
        response = telegram.send_message(settings.ADMIN_TG_ID, text)
        content.link.tg_message_id = get_telegram_message_id(response)

    if content.location:
        response = telegram.send_location(
            settings.ADMIN_TG_ID,
            latitude=content.location.lat,
            longitude=content.location.lon,
        )
        content.location.tg_message_id = get_telegram_message_id(response)
    logger.info(data)
    return data


def get_max_image_link(image: ImageSchema) -> str:
    max_size = max(image.sizes.keys(), key=lambda s: tuple(map(int, s.split('x'))))
    max_image_url = image.sizes[max_size]
    return max_image_url


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
    if data.content.image:
        content.image_id = await insert_image_to_db(data.content.image, session)
    if data.content.item:
        content.item_id = await insert_item_to_db(data.content.item, session)
    if data.content.link:
        content.link_id = await insert_link_to_db(data.content.link, session)
    if data.content.location:
        content.location_id = await insert_location_to_db(data.content.location, session)
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


async def insert_location_to_db(
        location: LocationSchema,
        session: AsyncSession = Depends(get_async_session)
):
    new_location = Location(
        **location.model_dump()
    )
    session.add(new_location)
    await session.commit()
    await session.refresh(new_location)
    return new_location.id


async def insert_link_to_db(
        link: LinkSchema,
        session: AsyncSession = Depends(get_async_session)
):
    link_preview_id = await insert_link_preview_to_db(link.preview, session)
    new_link = Link(
        text=link.text,
        url=link.url,
        preview_id=link_preview_id,
        tg_message_id=link.tg_message_id
    )
    session.add(new_link)
    await session.commit()
    await session.refresh(new_link)
    return new_link.id


async def insert_link_preview_to_db(
        link_preview: LinkPreviewSchema,
        session: AsyncSession = Depends(get_async_session)
) -> int:
    new_link_preview = LinkPreview(**link_preview.model_dump())
    session.add(new_link_preview)
    await session.commit()
    await session.refresh(new_link_preview)
    return new_link_preview.id


async def insert_item_to_db(
        item: ItemSchema,
        session: AsyncSession = Depends(get_async_session)
):
    new_item = Item(**item.model_dump())
    session.add(new_item)
    await session.commit()
    await session.refresh(new_item)
    return new_item.id


async def insert_image_to_db(
        image: ImageSchema,
        session: AsyncSession = Depends(get_async_session)
):
    new_image = Image(**image.model_dump())
    session.add(new_image)
    await session.commit()
    await session.refresh(new_image)
    return new_image.id


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
) -> int:
    await session.merge(Chat(id=data.chat_id, chat_type=data.chat_type))
    await session.commit()
    return data.chat_id


async def insert_message_to_db(
        message: CreateAvitoMessageSchema,
        session: AsyncSession = Depends(get_async_session)
):
    new_message = AvitoMessage(**message.model_dump())
    session.add(new_message)
    await session.commit()
