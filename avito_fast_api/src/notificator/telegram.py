from settings import settings
import requests


class TelegramNotificator:
    def __init__(self):
        self.bot_token = settings.BOT_TOKEN

    def send_message(self, chat_id, message):
        return requests.post(
            f"https://api.telegram.org/bot{self.bot_token}/sendMessage",
            data={"chat_id": chat_id, "text": message},
        )

    def send_picture(
        self,
        chat_id: str,
        image_url: str,
        caption: str | None = None,
    ):
        return requests.post(
            f"https://api.telegram.org/bot{self.bot_token}/sendPhoto",
            data={"chat_id": chat_id, "caption": caption, "photo": image_url}
        )
    def send_location(
            self,
            chat_id: str,
            latitude: str,
            longitude: str,
    ):
        return requests.post(
            f"https://api.telegram.org/bot{self.bot_token}/sendLocation",
            data={
                "chat_id": chat_id,
                "latitude": latitude,
                "longitude": longitude,
            }
        )


