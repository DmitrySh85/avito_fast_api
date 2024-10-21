from sqlalchemy.ext.asyncio import AsyncSession
from tokens.services import get_token
from fastapi import Depends
from db import get_async_session
import requests
from logger import logger


class AvitoItemManager:

    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self.session = session

    async def get_item_from_avito(self, item_id: int):
        items = await self.get_items_from_avito()
        matched_items = list(filter(lambda item: item.get("id") == item_id, items))

        if matched_items:
            logger.info(matched_items[0])
            return matched_items[0]

    async def get_authorization_token(self):
        token = await get_token(self.session)
        return token

    async def get_items_from_avito(self):
        authorization_token = await self.get_authorization_token()
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

