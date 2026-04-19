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

    return templates.TemplateResponse(request, "home.html")
# Add this NEW section right below it
@app.get("/login-page")
def login_page(request: Request):

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


# Add these to your main.py (right where your other @app.get routes are)

@app.get("/report-page")
def report_p(request: Request):
    return templates.TemplateResponse(request, "report.html")

@app.get("/resource-page")
def resource_p(request: Request):
    return templates.TemplateResponse(request, "resource.html")

@app.get("/allocation-page")
def allocation_p(request: Request):
    return templates.TemplateResponse(request, "allocation.html")

@app.get("/volunteer-page")
def volunteer_p(request: Request):
    return templates.TemplateResponse(request, "volunteer_mgmt.html")

@app.get("/tracking-page")
def tracking_p(request: Request):
    return templates.TemplateResponse(request, "tracking.html")

@app.get("/access-page")
def access_p(request: Request):
    return templates.TemplateResponse(request, "access.html")

@app.get("/reports-page")
def reports_p(request: Request):
    return templates.TemplateResponse(request, "reports.html")

# THIS PART TELLS PYTHON HOW TO RUN THE FILE DIRECTLY
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

