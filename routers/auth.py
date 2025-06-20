from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
from schemas import UserCreate, Token, UserLogin
from core.security import hash_password, verify_password, create_token

router = APIRouter()

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

@router.post("/register", response_model=Token)
def register(u: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter_by(username=u.username).first():
        raise HTTPException(400, "Username exists")
    user = User(
        username=u.username,
        hashed_password=hash_password(u.password),
        controller_token=u.controller_token
    )
    db.add(user); db.commit(); db.refresh(user)
    token = create_token({"sub": user.username})
    return Token(access_token=token)

@router.post("/login", response_model=Token)
def login(u: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(username=u.username).first()
    if not user or not verify_password(u.password, user.hashed_password):
        raise HTTPException(400, "Invalid credentials")
    return Token(access_token=create_token({"sub": user.username}))
