from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from database import engine
import models, auth, routes

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(auth.router)
app.include_router(routes.router)

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/register-page")
def reg_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/dashboard")
def dash(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})