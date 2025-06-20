from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import ControllerConfig
from schemas import ConfigResponse

router = APIRouter()

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

@router.get("/get-config", response_model=ConfigResponse)
def get_config(token: str, db: Session = Depends(get_db)):
    cfg = db.query(ControllerConfig).filter_by(controller_token=token).first()
    if not cfg:
        raise HTTPException(404, "Not found")
    return ConfigResponse(controller_token=cfg.controller_token, setting_1=cfg.setting_1, active=cfg.active)
