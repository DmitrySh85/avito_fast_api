from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from tokens.services import get_token
from fastapi import Depends
from db import get_async_session
import requests
from logger import logger
from message.schemas import AvitoMessageSchema
from message.models import Content, AvitoMessage


class AvitoItemManager:

    def __init__(
            self,
            session: AsyncSession = Depends(get_async_session)
    ):
        self.session = session

    async def get_item_from_avito(
            self,
            item_id: int,
            department_id: int

    ):
        items = await self.get_items_from_avito(department_id)
        print(items)
        matched_items = list(filter(lambda item: item.get("id") == item_id, items))

        if matched_items:
            return matched_items[0]

    async def get_messages_in_post(self, data: AvitoMessageSchema):
        avito_chat_id = data.chat_id
        logger.info(avito_chat_id)
        stmt = select(Content.tg_message_id
                      ).join(AvitoMessage, AvitoMessage.content_id == Content.id
                             ).where(AvitoMessage.chat_id == avito_chat_id
                                     )
        result = await self.session.execute(stmt)
        return result.scalar()

    async def get_authorization_token(self, department_id: int):
        token = await get_token(department_id, self.session)
        return token

    async def get_items_from_avito(self, department_id: int):
        authorization_token = await self.get_authorization_token(department_id)
        headers = {"Authorization": f"Bearer {authorization_token}"}
        params = {"per_page": 100}
        url = "https://api.avito.ru/core/v1/items"
        try:
            response = requests.get(url=url, headers=headers, params=params)
        except Exception as e:
            logger.info(e)
            return []
        logger.info(response)
        data = response.json()
        logger.info(data.get("per_page"))
        items = data.get("resources", [])
        logger.info(len(items))
        return items
