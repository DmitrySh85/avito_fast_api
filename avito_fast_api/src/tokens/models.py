from db import Base
from sqlalchemy import Column, String, DateTime, Integer


class AccessToken(Base):
    __tablename__ = "token"
    id = Column(Integer(), primary_key=True, autoincrement=True)
    token = Column(String())
    expires_at = Column(DateTime())