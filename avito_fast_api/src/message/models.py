from db import Base
from sqlalchemy import Column, Integer, String, JSON, Text, ForeignKey, Float, BigInteger
from sqlalchemy.orm import relationship


class Call(Base):
    __tablename__ = 'calls'

    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(String, nullable=False)
    target_user_id = Column(Integer, nullable=False)
    tg_message_id = Column(BigInteger, nullable=True)


class Image(Base):
    __tablename__ = 'images'

    id = Column(Integer, primary_key=True, autoincrement=True)
    sizes = Column(JSON, nullable=False)
    tg_message_id = Column(BigInteger, nullable=False)


class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True, autoincrement=True)
    image_url = Column(String, nullable=False)
    item_url = Column(String, nullable=False)
    price_string = Column(String, nullable=False)
    title = Column(String, nullable=False)
    tg_message_id = Column(BigInteger, nullable=True)


class LinkPreview(Base):
    __tablename__ = 'link_previews'

    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(Text, nullable=False)
    domain = Column(String, nullable=False)
    images = Column(JSON, nullable=False)
    title = Column(String, nullable=True)
    url = Column(String, nullable=True)


class Link(Base):
    __tablename__ = 'links'

    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(Text, nullable=False)
    url = Column(String, nullable=False)
    preview_id = Column(Integer, ForeignKey('link_previews.id'), nullable=True)
    tg_message_id = Column(BigInteger, nullable=False)
    preview = relationship('LinkPreview', backref='links')


class Location(Base):
    __tablename__ = 'locations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    kind = Column(String, nullable=False)
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)
    text = Column(Text, nullable=True)
    title = Column(String, nullable=True)
    tg_message_id = Column(Integer, nullable=False)


class Content(Base):
    __tablename__ = 'contents'

    id = Column(Integer, primary_key=True, autoincrement=True)
    call_id = Column(Integer, ForeignKey('calls.id'), nullable=True)
    image_id = Column(Integer, ForeignKey('images.id'), nullable=True)
    item_id = Column(Integer, ForeignKey('items.id'), nullable=True)
    link_id = Column(Integer, ForeignKey('links.id'), nullable=True)
    location_id = Column(Integer, ForeignKey('locations.id'), nullable=True)
    text = Column(Text, nullable=True)
    tg_message_id = Column(Integer, nullable=False)

    call = relationship('Call', backref='contents')
    image = relationship('Image', backref='contents')
    item = relationship('Item', backref='contents')
    link = relationship('Link', backref='contents')
    location = relationship('Location', backref='contents')


class Chat(Base):
    __tablename__ = 'chats'
    id = Column(String, primary_key=True)
    chat_type = Column(String, nullable=False)


class AvitoMessage(Base):
    __tablename__ = 'avito_messages'

    id = Column(String, primary_key=True)
    author_id = Column(Integer, nullable=False)
    chat_id = Column(String, ForeignKey('chats.id'), nullable=False)
    content_id = Column(Integer, ForeignKey('contents.id'), nullable=False)
    created = Column(Integer, nullable=False)
    item_id = Column(Integer, nullable=False)
    read = Column(Integer, nullable=False)
    type = Column(String, nullable=False)
    user_id = Column(Integer, nullable=False)

    content = relationship('Content', backref='avito_messages')
    chat = relationship('Chat', backref='avito_messages')


