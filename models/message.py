from sqlalchemy import Column, String, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from database import Base

class Message(Base):
    __tablename__ = "messages"
    id = Column(String(36), primary_key=True, default=str(uuid4()))
    sender_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    receiver_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    book_id = Column(String(36), ForeignKey("books.id"), nullable=True)
    content = Column(Text, nullable=False)
    sent_at = Column(DateTime, server_default=func.now())