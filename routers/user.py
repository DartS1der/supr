from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User, ControllerConfig
from schemas import Config, ConfigResponse
from fastapi.security import OAuth2PasswordBearer
from core.security import decode_token

router = APIRouter()
oauth = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

def get_user(token: str = Depends(oauth), db: Session = Depends(get_db)):
    data = decode_token(token)
    user = db.query(User).filter_by(username=data["sub"]).first()
    if not user: raise HTTPException(401, "Invalid token")
    return user

@router.post("/set-config", response_model=ConfigResponse)
def set_config(c: Config, user: User = Depends(get_user), db: Session = Depends(get_db)):
    cfg = user.config or ControllerConfig(
        controller_token=user.controller_token, owner=user
    )
    cfg.setting_1 = c.setting_1
    cfg.active = c.active
    db.add(cfg); db.commit(); db.refresh(cfg)
    return ConfigResponse(controller_token=user.controller_token, setting_1=cfg.setting_1, active=cfg.active)
