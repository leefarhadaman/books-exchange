from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models.wishlist import Wishlist
from schemas.wishlist import WishlistCreate, WishlistResponse
from auth import get_current_user
from database import get_db

router = APIRouter(prefix="/wishlist", tags=["wishlist"])

@router.post("/", response_model=WishlistResponse)
def add_to_wishlist(wishlist: WishlistCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_wishlist = Wishlist(book_id=wishlist.book_id, user_id=current_user.id)
    db.add(db_wishlist)
    db.commit()
    db.refresh(db_wishlist)
    return db_wishlist

@router.get("/", response_model=list[WishlistResponse])
def get_wishlist(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Wishlist).filter(Wishlist.user_id == current_user.id).all()