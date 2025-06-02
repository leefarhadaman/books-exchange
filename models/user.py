from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func
from uuid import uuid4
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(String(36), primary_key=True, default=str(uuid4()))
    email = Column(String(255), unique=True, nullable=False)  # Encrypted in DB
    password_hash = Column(String(255), nullable=False)
    username = Column(String(100), nullable=False)
    college = Column(String(100), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
