from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session
from database import SessionLocal
import models, utils

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register")
def register(name: str = Form(...), email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = models.User(
        name=name,
        email=email,
        password=utils.hash_password(password),
        role="user"
    )
    db.add(user)
    db.commit()
    return {"msg": "Registered"}

@router.post("/login")
def login(email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == email).first()
    if user and utils.verify_password(password, user.password):
        return {"msg": "success", "role": user.role}
    return {"msg": "invalid"}