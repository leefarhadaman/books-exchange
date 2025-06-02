from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from database import Base

class Wishlist(Base):
    __tablename__ = "wishlists"
    id = Column(String(36), primary_key=True, default=str(uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    book_id = Column(String(36), ForeignKey("books.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())