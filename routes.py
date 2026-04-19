from fastapi import APIRouter, Depends, Form, Request
from sqlalchemy.orm import Session
from sqlalchemy import case
from database import SessionLocal
import models
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------- REQUEST ----------------
@router.post("/request")
def create_request(
    resource_id: int = Form(...),
    quantity: int = Form(...),
    priority: str = Form(...),
    db: Session = Depends(get_db)
):
    req = models.Request(
        user_id=1,
        resource_id=resource_id,
        quantity=quantity,
        priority=priority
    )
    db.add(req)
    db.commit()
    return {"msg": "Request added successfully"}


# ---------------- ALLOCATION ----------------
@router.get("/allocate")
def allocate(db: Session = Depends(get_db)):
    reqs = db.query(models.Request).order_by(
        case(
            (models.Request.priority == "high", 1),
            (models.Request.priority == "medium", 2),
            else_=3
        )
    ).all()

    for r in reqs:
        res = db.query(models.Resource).filter(
            models.Resource.id == r.resource_id
        ).first()

        if res and res.quantity >= r.quantity:
            res.quantity -= r.quantity
            r.status = "approved"
        else:
            r.status = "rejected"

    db.commit()
    return {"msg": "Allocation completed"}


# ---------------- REPORTS ----------------
@router.get("/reports")
def view_reports(request: Request, db: Session = Depends(get_db)):
    reqs = db.query(models.Request).all()

    return templates.TemplateResponse(
        "reports.html",
        {
            "request": request,
            "requests": reqs
        }
    )