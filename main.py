from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from database import engine
import models
import auth
import routes

# Create tables
models.Base.metadata.create_all(bind=engine)

# FastAPI app
app = FastAPI()

# Templates
templates = Jinja2Templates(directory="templates")

# Static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routers
app.include_router(auth.router)
app.include_router(routes.router)

# Home page (login)
@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# Register page
@app.get("/register-page")
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

# Dashboard (protected)
@app.get("/dashboard")
def dashboard(request: Request):
    user_id = request.cookies.get("user_id")

    if not user_id:
        return RedirectResponse(url="/")

    return templates.TemplateResponse("dashboard.html", {"request": request})