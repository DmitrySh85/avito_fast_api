from pydantic import BaseModel, Field
from typing import Optional, List



class TelegramLocationSchema(BaseModel):
    longitude: float
    latitude: float


class TelegramPhotoSchema(BaseModel):
    file_id: str
    file_unique_id: str
    width: int
    height: int
    file_size: int


class TelegramUserSchema(BaseModel):
    id: int
    is_bot: bool
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None
    language_code: Optional[str] = None


class TelegramChatSchema(BaseModel):
    id: int
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None
    type: str


class TelegramReplyToMessageSchema(BaseModel):
    message_id: int
    from_user: TelegramUserSchema = Field(alias="from")
    chat: TelegramChatSchema
    date: int
    location: Optional[TelegramLocationSchema] = None
    photo: Optional[list[TelegramPhotoSchema]] = None

    class Config:
        populate_by_name = True


class MessageSchema(BaseModel):
    message_id: int
    from_user: TelegramUserSchema = Field(alias="from")
    chat: TelegramChatSchema
    date: int
    text: Optional[str] = None
    reply_to_message: Optional[TelegramReplyToMessageSchema] = None

    class Config:
        populate_by_name = True


class UpdateSchema(BaseModel):
    update_id: int
    message: MessageSchema


class SendMessageToAvitoSchema(BaseModel):
    token: str
    chat_id: str
    user_id: int
    text: str