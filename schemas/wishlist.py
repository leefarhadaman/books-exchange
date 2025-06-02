from pydantic import BaseModel
from enum import Enum
from datetime import datetime

class BookCondition(str, Enum):
    New = "New"
    Good = "Good"
    Fair = "Fair"

class OwnerHistory(str, Enum):
    First = "First"
    Second = "Second"
    Third = "Third"
    MoreThanThree = "MoreThanThree"

class BookStatus(str, Enum):
    Available = "Available"
    Sold = "Sold"
    Traded = "Traded"

class BookBase(BaseModel):
    title: str
    author: str
    isbn: str | None = None
    course: str | None = None
    condition: BookCondition
    original_price: float | None = None
    price: float | None = None
    owner_history: OwnerHistory

class BookCreate(BookBase):
    pass

class BookResponse(BookBase):
    id: str
    seller_id: str
    status: BookStatus
    created_at: str

    class Config:
        from_attributes = True