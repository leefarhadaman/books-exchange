from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from models.book import Book
from schemas.book import BookCreate, BookResponse
from auth import get_current_user
from database import get_db
import bleach

router = APIRouter(prefix="/books", tags=["books"])

@router.post("/", response_model=BookResponse)
def create_book(book: BookCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Sanitize inputs
    book.title = bleach.clean(book.title)
    book.author = bleach.clean(book.author)
    book.isbn = bleach.clean(book.isbn) if book.isbn else None
    book.course = bleach.clean(book.course) if book.course else None
    
    db_book = Book(**book.dict(), seller_id=current_user.id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

@router.get("/search", response_model=list[BookResponse])
def search_books(query: str, db: Session = Depends(get_db)):
    query = bleach.clean(query)
    sql = text("SELECT * FROM books WHERE MATCH(title, author, isbn) AGAINST(:query IN BOOLEAN MODE)")
    result = db.execute(sql, {"query": query}).mappings().all()
    return result