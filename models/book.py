from sqlalchemy import Column, String, Enum, Float, ForeignKey, DateTime
from sqlalchemy.sql import func
from database import Base
import enum

class BookCondition(enum.Enum):
    New = "New"
    Good = "Good"
    Fair = "Fair"

class OwnerHistory(enum.Enum):
    First = "First"
    Second = "Second"
    Third = "Third"
    MoreThanThree = "MoreThanThree"

class BookStatus(enum.Enum):
    Available = "Available"
    Sold = "Sold"
    Traded = "Traded"

class Book(Base):
    __tablename__ = "books"
    id = Column(String(36), primary_key=True, default=str(uuid4()))
    title = Column(String(255), nullable=False)
    author = Column(String(255), nullable=False)
    isbn = Column(String(13), nullable=True)
    course = Column(String(50), nullable=True)
    condition = Column(Enum(BookCondition), nullable=False)
    original_price = Column(Float, nullable=True)
    price = Column(Float, nullable=True)
    owner_history = Column(Enum(OwnerHistory), nullable=False)
    seller_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    status = Column(Enum(BookStatus), default=BookStatus.Available)
    created_at = Column(DateTime, server_default=func.now())
