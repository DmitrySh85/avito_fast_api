from db import Base
from sqlalchemy import Column, Integer, String, JSON, Text, ForeignKey, Float, BigInteger, DateTime
from sqlalchemy.orm import relationship


class Call(Base):
    __tablename__ = 'calls'

    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(String, nullable=False)
    target_user_id = Column(Integer, nullable=False)
    tg_message_id = Column(BigInteger, nullable=True)


class Content(Base):
    __tablename__ = 'contents'

    id = Column(Integer, primary_key=True, autoincrement=True)
    call_id = Column(Integer, ForeignKey('calls.id'), nullable=True)
    text = Column(Text, nullable=True)
    tg_message_id = Column(Integer, nullable=False)
    call = relationship('Call', backref='contents')


class Chat(Base):
    __tablename__ = 'chats'
    id = Column(String, primary_key=True)
    chat_type = Column(String, nullable=False)
    telegram_topic = Column(BigInteger())
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)

    department = relationship("Department", backref="chats")


class AvitoMessage(Base):
    __tablename__ = 'avito_messages'

    id = Column(String, primary_key=True)
    author_id = Column(BigInteger, nullable=False)
    chat_id = Column(String, ForeignKey('chats.id'), nullable=False)
    content_id = Column(Integer, ForeignKey('contents.id'), nullable=False)
    created = Column(Integer, nullable=False)
    item_id = Column(BigInteger, nullable=False)
    read = Column(Integer, nullable=True)
    type = Column(String, nullable=False)
    user_id = Column(BigInteger, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=True)

    content = relationship('Content', backref='avito_messages')
    chat = relationship('Chat', backref='avito_messages')


