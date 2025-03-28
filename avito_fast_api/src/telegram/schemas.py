from pydantic import BaseModel, Field
from typing import Optional, List

class TelegramEventSchema(BaseModel):
    chat_id: str
    text: str


class SendMessageToAvitoSchema(BaseModel):
    token: str
    chat_id: str
    user_id: int
    text: str