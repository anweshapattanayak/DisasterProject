from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from database import engine, Base
import models
import auth
import routes

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(routes.router)


@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <h1>Disaster Management System 🚀</h1>
    <p>API is running successfully</p>
    <a href="/docs">Go to API Docs</a><br>
    <a href="/reports/">View Reports</a>
    """