from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str
    controller_token: str

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str

class Config(BaseModel):
    setting_1: str
    active: bool

class ConfigResponse(Config):
    controller_token: str
