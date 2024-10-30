import datetime
from uuid import UUID

from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime


class CallSchema(BaseModel):
    status: str
    target_user_id: int
    tg_message_id: Optional[int] = None


class ContentSchema(BaseModel):
    call: Optional[CallSchema] = None
    text: Optional[str] = None
    tg_message_id: Optional[int] = None


class CreateContentSchema(BaseModel):
    call_id: Optional[int] = None
    text: Optional[str] = None
    tg_message_id: Optional[int] = None


class AvitoMessageSchema(BaseModel):
    author_id: int
    chat_id: str
    chat_type: str
    telegram_topic: Optional[int] = None
    content: ContentSchema
    created: int
    id: str
    item_id: int
    read: Optional[int] = None
    type: str
    user_id: int
    published_at: Optional[datetime]


class ObjectPayload(BaseModel):
    type: str
    value: AvitoMessageSchema


class Object(BaseModel):
    id: UUID
    version: Optional[str]
    timestamp: int
    payload: ObjectPayload


class CreateAvitoMessageSchema(BaseModel):
    author_id: int
    content_id: int
    chat_id: str
    telegram_topic: Optional[int] = None
    created: int
    id: str
    item_id: int
    read: Optional[int] = None
    type: str
    user_id: int
    created_at: Optional[datetime] = None


