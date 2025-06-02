from sqlalchemy import Column, String, Enum, ForeignKey, DateTime
from sqlalchemy.sql import func
from database import Base
import enum

class RequestStatus(enum.Enum):
    Pending = "Pending"
    Accepted = "Accepted"
    Rejected = "Rejected"

class Request(Base):
    __tablename__ = "requests"
    id = Column(String(36), primary_key=True, default=str(uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    book_id = Column(String(36), ForeignKey("books.id"), nullable=False)
    status = Column(Enum(RequestStatus), default=RequestStatus.Pending)
    created_at = Column(DateTime, server_default=func.now())