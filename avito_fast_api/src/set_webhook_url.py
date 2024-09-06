import requests
from token.services import get_access_token
from settings import settings
from logger import logger

def set_webhook_url():
    logger.info(f"Setting webhook: {settings.WEBHOOK_URL}")
    url = "https://api.avito.ru/messenger/v3/webhook"
    access_token = get_access_token()
    headers = {"Authorization": f"Bearer {access_token}"}
    data = {
        "url": settings.WEBHOOK_URL
    }
    response = requests.post(url, headers=headers, data=data)
    logger.info(response.json())


if __name__ == "__main__":
    set_webhook_url()