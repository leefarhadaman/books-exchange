from pydantic import BaseModel
from enum import Enum

class RequestStatus(str, Enum):
    Pending = "Pending"
    Accepted = "Accepted"
    Rejected = "Rejected"

class RequestBase(BaseModel):
    book_id: str

class RequestCreate(RequestBase):
    pass

class RequestResponse(RequestBase):
    id: str
    user_id: str
    status: RequestStatus
    created_at: str

    class Config:
        from_attributes = True