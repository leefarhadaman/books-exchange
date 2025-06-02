from fastapi import APIRouter, Depends, WebSocket
from sqlalchemy.orm import Session
from models.message import Message
from schemas.message import MessageCreate, MessageResponse
from auth import get_current_user
from database import get_db
import bleach

router = APIRouter(prefix="/messages", tags=["messages"])

@router.post("/", response_model=MessageResponse)
def send_message(message: MessageCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    message.content = bleach.clean(message.content)
    db_message = Message(**message.dict(), sender_id=current_user.id)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

@router.get("/", response_model=list[MessageResponse])
def get_conversation(receiver_id: str, book_id: str | None = None, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    query = db.query(Message).filter(
        ((Message.sender_id == current_user.id) & (Message.receiver_id == receiver_id)) |
        ((Message.sender_id == receiver_id) & (Message.receiver_id == current_user.id))
    )
    if book_id:
        query = query.filter(Message.book_id == book_id)
    return query.all()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, db: Session = Depends(get_db)):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            message = MessageCreate(**data)
            message.content = bleach.clean(message.content)
            db_message = Message(**message.dict(), sender_id=data["sender_id"])
            db.add(db_message)
            db.commit()
            await websocket.send_json({"status": "Message sent"})
    except Exception:
        await websocket.close()