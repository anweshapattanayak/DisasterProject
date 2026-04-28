from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
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


# ---------------- REGISTER ----------------
@router.post("/register")
def register(
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = models.User(
        name=name,
        email=email,
        password=utils.hash_password(password),
        role="user"
    )

    db.add(user)
    db.commit()

    return RedirectResponse("/login-page", status_code=302)


# ---------------- LOGIN (FIXED - SESSION ONLY) ----------------
# ---------------- LOGIN ----------------
@router.post("/login")
def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.email == email).first()

    if user and utils.verify_password(password, user.password):

        request.session["user_id"] = user.id
        request.session["role"] = user.role

        # ✅ RETURN TO WHERE USER CAME FROM
        next_page = request.session.pop("next", None)
        if next_page:
            return RedirectResponse(next_page, status_code=302)

        # ✅ ROLE BASED REDIRECT
        if user.role == "volunteer":
            return RedirectResponse("/reports-page", status_code=302)

        # ✅ USER + ADMIN → GO TO HOME (FEATURE SECTION)
        return RedirectResponse("/", status_code=302)

    return RedirectResponse("/login-page", status_code=302)