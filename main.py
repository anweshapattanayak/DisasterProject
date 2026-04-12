from fastapi import FastAPI
from database import engine, Base
import models

import auth
import routes

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(routes.router)


@app.get("/")
def home():
    return {"message": "API running"}