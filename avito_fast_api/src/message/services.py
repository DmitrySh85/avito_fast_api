from .schemas import ObjectSchema, ImageSchema
from notificator.telegram import TelegramNotificator
from settings import settings
from static_text.static_text import MESSAGE_RECEIVED


def send_data_to_tg(data: ObjectSchema):
    telegram = TelegramNotificator()
    content = data.content
    telegram.send_message(settings.ADMIN_TG_ID, MESSAGE_RECEIVED)
    if content.text:
        telegram.send_message(settings.ADMIN_TG_ID, content.text)
    if data.content.image:
        max_image_link = get_max_image_link(content.image)
        telegram.send_picture(settings.ADMIN_TG_ID, max_image_link)
    if content.item:
        caption = f"{content.item.title} {content.item.price_string} {content.item.item_url}".strip()
        telegram.send_picture(settings.ADMIN_TG_ID, content.item.image_url, caption)
    if content.link:
        text = f"{content.link.text} {content.link.url}"
        telegram.send_message(settings.ADMIN_TG_ID, text)
    if content.location:
        caption = f"{content.location.title} {content.location.text}".strip()
        print(caption)
        telegram.send_location(
            settings.ADMIN_TG_ID,
            latitude=content.location.lat,
            longitude=content.location.lon,
        )

def get_max_image_link(image: ImageSchema) -> str:
    max_size = max(image.sizes.keys(), key=lambda s: tuple(map(int, s.split('x'))))
    max_image_url = image.sizes[max_size]
    return max_image_url

