from db import Base
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey


class Review(Base):
    __tablename__ = "review"
    id = Column(Integer(), primary_key=True, autoincrement=True)
    score = Column(Integer())
    stage = Column(String())
    text = Column(String())
    used_in_score = Column(Boolean(), default=True)
    can_answer = Column(Boolean(), default=True)
    created_at = Column(TIMESTAMP)
    department = Column(ForeignKey("departments.id"), nullable=False)