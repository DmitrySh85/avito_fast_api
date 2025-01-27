from db import Base
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship


class AccessToken(Base):
    __tablename__ = "token"
    id = Column(Integer(), primary_key=True, autoincrement=True)
    token = Column(String())
    expires_at = Column(DateTime())
    department_id = Column(Integer(), ForeignKey('departments.id'), nullable=True)

    departments = relationship("Department", backref="tokens")