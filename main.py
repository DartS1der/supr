
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Псевдо-хранилище
settings_db = {
    "controller1": {"volume": 70, "mode": "auto"},
    "controller2": {"volume": 20, "mode": "manual"}
}

class SettingsPayload(BaseModel):
    settings: dict

@app.get("/controller", response_class=HTMLResponse)
async def controller_page(request: Request):
    return templates.TemplateResponse("controller.html", {"request": request})

@app.get("/user", response_class=HTMLResponse)
async def user_page(request: Request):
    return templates.TemplateResponse("user.html", {"request": request})

@app.get("/api/get_settings/{token}")
async def get_settings(token: str):
    return {"settings": settings_db.get(token, {})}

@app.post("/api/update_settings/{token}")
async def update_settings(token: str, payload: SettingsPayload):
    settings_db[token] = payload.settings
    return {"status": "ok"}
