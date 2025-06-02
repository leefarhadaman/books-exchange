from pydantic import BaseModel

class MessageBase(BaseModel):
    receiver_id: str
    book_id: str | None = None
    content: str

class MessageCreate(MessageBase):
    pass

class MessageResponse(MessageBase):
    id: str
    sender_id: str
    sent_at: str

    class Config:
        from_attributes = True