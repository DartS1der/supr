from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    controller_token = Column(String, unique=True, index=True)
    config = relationship("ControllerConfig", back_populates="owner", uselist=False)

class ControllerConfig(Base):
    __tablename__ = "controller_configs"
    id = Column(Integer, primary_key=True, index=True)
    controller_token = Column(String, unique=True, index=True)
    setting_1 = Column(String, default="value")
    active = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="config")
