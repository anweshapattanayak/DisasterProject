from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from database import engine
import models, auth, routes

# Create tables in the DB
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Try to mount static folder (if you have one)
try:
    app.mount("/static", StaticFiles(directory="static"), name="static")
except:
    pass

app.include_router(auth.router)
app.include_router(routes.router)

@app.get("/")
def home(request: Request):
    # 'request' must come first in this version
    return templates.TemplateResponse(request, "login.html")

@app.get("/register-page")
def reg_page(request: Request):
    return templates.TemplateResponse(request, "register.html")

@app.get("/dashboard")
def dash(request: Request):
    return templates.TemplateResponse(request, "dashboard.html")

# THIS PART TELLS PYTHON HOW TO RUN THE FILE DIRECTLY
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)