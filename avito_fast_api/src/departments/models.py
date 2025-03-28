from db import Base
from sqlalchemy import Column, Integer, String, BigInteger


class Department(Base):
    __tablename__ = 'departments'
    id = Column(Integer(), primary_key=True)
    name = Column(String())
    address = Column(String())
    telegram_group_id = Column(BigInteger())

