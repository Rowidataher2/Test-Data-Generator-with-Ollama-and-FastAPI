from sqlalchemy import Column, Integer, Text, TIMESTAMP
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from .database import Base

class Request(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    user_request = Column(Text, nullable=False)
    messages = Column(JSONB, nullable=False)  # full chat history
    response = Column(JSONB, nullable=False)  # parsed JSON result
    created_at = Column(TIMESTAMP, server_default=func.now())
