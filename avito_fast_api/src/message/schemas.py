from pydantic import BaseModel
from typing import Optional, Dict


class CallSchema(BaseModel):
    status: str
    target_user_id: int
    tg_message_id: Optional[int] = None


class ImageSchema(BaseModel):
    sizes: Dict[str, str]
    tg_message_id: Optional[int] = None


class ItemSchema(BaseModel):
    image_url: str
    item_url: str
    price_string: str
    title: str
    tg_message_id: Optional[int] = None


class LinkPreviewSchema(BaseModel):
    description: str
    domain: str
    images: Dict[str, str]
    title: Optional[str] = None
    url: str


class LinkSchema(BaseModel):
    preview: Optional[LinkPreviewSchema] = None
    text: str
    url: str
    tg_message_id: Optional[int] = None


class LocationSchema(BaseModel):
    kind: str
    lat: float
    lon: float
    text: Optional[str] = None
    title: Optional[str] = None
    tg_message_id: Optional[int] = None



class ContentSchema(BaseModel):
    call: Optional[CallSchema] = None
    image: Optional[ImageSchema] = None
    item: Optional[ItemSchema] = None
    link: Optional[LinkSchema] = None
    location: Optional[LocationSchema] = None
    text: Optional[str] = None
    tg_message_id: Optional[int] = None


class CreateContentSchema(BaseModel):
    call_id: Optional[int] = None
    image_id: Optional[int] = None
    item_id: Optional[int] = None
    link_id: Optional[int] = None
    location_id: Optional[int] = None
    text: Optional[str] = None
    tg_message_id: Optional[int] = None


class AvitoMessageSchema(BaseModel):
    author_id: int
    chat_id: str
    chat_type: str
    content: ContentSchema
    created: int
    id: str
    item_id: int
    read: int
    type: str
    user_id: int


class CreateAvitoMessageSchema(BaseModel):
    author_id: int
    content_id: int
    chat_id: str
    created: int
    id: str
    item_id: int
    read: int
    type: str
    user_id: int


