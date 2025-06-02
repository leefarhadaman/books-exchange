from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from models.user import User
from schemas.user import UserCreate, UserResponse
from auth import get_password_hash, encrypt_email, create_access_token, create_refresh_token, get_current_user, decrypt_email
from database import get_db
import bleach

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    # Sanitize inputs
    user.email = bleach.clean(user.email)
    user.username = bleach.clean(user.username)
    user.college = bleach.clean(user.college) if user.college else None
    
    # Check if email exists
    existing_user = db.query(User).filter(User.email == encrypt_email(user.email)).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
    # Create user
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=encrypt_email(user.email),
        password_hash=hashed_password,
        username=user.username,
        college=user.college
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == encrypt_email(form_data.username)).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": user.id})
    refresh_token = create_refresh_token(data={"sub": user.id})
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}