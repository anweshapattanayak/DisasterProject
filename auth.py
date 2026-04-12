from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session
from database import get_db
import models
from passlib.context import CryptContext

router = APIRouter(prefix="/auth")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/register")
def register(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.username == username).first()

    if user:
        return {"message": "User already exists"}

    hashed = pwd_context.hash(password)

    new_user = models.User(
        username=username,
        hashed_password=hashed
    )

    db.add(new_user)
    db.commit()

    return {"message": "User created successfully"}


@router.post("/login")
def login(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.username == username).first()

    if not user:
        return {"message": "Invalid user"}

    if not pwd_context.verify(password, user.hashed_password):
        return {"message": "Wrong password"}

    return {"message": "Login successful"}