from pydantic import BaseModel
from typing import Optional, Dict


class CallSchema(BaseModel):
    status: str
    target_user_id: int


class ImageSchema(BaseModel):
    sizes: Dict[str, str]


class ItemSchema(BaseModel):
    image_url: str
    item_url: str
    price_string: str
    title: str


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


class LocationSchema(BaseModel):
    kind: str
    lat: float
    lon: float
    text: Optional[str] = None
    title: Optional[str] = None


class ContentSchema(BaseModel):
    call: Optional[CallSchema] = None
    image: Optional[ImageSchema] = None
    item: Optional[ItemSchema] = None
    link: Optional[LinkSchema] = None
    location: Optional[LocationSchema] = None
    text: Optional[str] = None


class ObjectSchema(BaseModel):
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



