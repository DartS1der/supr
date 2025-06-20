from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import Column, Integer, String, JSON, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

app = FastAPI()

# CORS на всякий случай
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Настройки базы данных
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Controller(Base):
    __tablename__ = "controllers"
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, index=True)
    settings = Column(JSON)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/api/get_settings/{token}")
async def get_settings(token: str, db: Session = Depends(get_db)):
    controller = db.query(Controller).filter(Controller.token == token).first()
    if not controller:
        raise HTTPException(status_code=404, detail="Контроллер не найден")
    return {"settings": controller.settings or {}}

@app.post("/api/update_settings/{token}")
async def update_settings(token: str, payload: dict, db: Session = Depends(get_db)):
    controller = db.query(Controller).filter(Controller.token == token).first()
    if not controller:
        raise HTTPException(status_code=404, detail="Контроллер не найден")
    controller.settings = payload["settings"]
    db.commit()
    return {"message": "Настройки обновлены"}

# Подключаем интерфейс
app.mount("/", StaticFiles(directory="static", html=True), name="static")