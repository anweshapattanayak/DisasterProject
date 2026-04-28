from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware

from database import engine
import models
import auth
import routes

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# SESSION
app.add_middleware(SessionMiddleware, secret_key="super-secret-key")

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(auth.router)
app.include_router(routes.router)


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request,
        "home.html",
        {"request": request}
    )


@app.get("/dashboard")
def dashboard(request: Request):
    return templates.TemplateResponse(
        request,
        "dashboard.html",
        {"request": request}
    )



@app.get("/volunteer-page")
def volunteer_page(request: Request):
    return templates.TemplateResponse(
        request,
        "volunteer_mgmt.html",
        {"request": request}
    )


@app.get("/access-page")
def access_page(request: Request):
    return templates.TemplateResponse(
        request,
        "access.html",
        {"request": request}
    )