
from fastapi import APIRouter, Depends, Form, Request

from fastapi import APIRouter, Depends, Form

from sqlalchemy.orm import Session
from sqlalchemy import case
from database import SessionLocal
import models

from fastapi.templating import Jinja2Templates

router = APIRouter()

# Template setup
templates = Jinja2Templates(directory="templates")


# Database connection


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# Create request
@router.post("/request")
def create_request(
    resource_id: int = Form(...),
    quantity: int = Form(...),
    priority: str = Form(...),
    db: Session = Depends(get_db)
):

@router.post("/request")
def create_request(resource_id: int = Form(...), quantity: int = Form(...), priority: str = Form(...), db: Session = Depends(get_db)):

    req = models.Request(
        user_id=1,
        resource_id=resource_id,
        quantity=quantity,
        priority=priority
    )
    db.add(req)
    db.commit()

    return {"msg": "Request added successfully"}


# Allocation logic
@router.get("/allocate")
def allocate(db: Session = Depends(get_db)):
    reqs = db.query(models.Request).order_by(

    return {"msg": "request added"}

@router.get("/allocate")
def allocate(db: Session = Depends(get_db)):

    reqs = db.query(models.Request).filter(
        models.Request.status == "pending"
    ).order_by(

        case(
            (models.Request.priority == "high", 1),
            (models.Request.priority == "medium", 2),
            else_=3
        )
    ).all()


    result = []

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


# Reports page
@router.get("/reports")
def view_reports(request: Request, db: Session = Depends(get_db)):
    reqs = db.query(models.Request).all()

    return templates.TemplateResponse(
        "reports.html",
        {
            "request": request,
            "requests": reqs
        }

        if res:
            if res.quantity >= r.quantity:
                res.quantity -= r.quantity
                r.status = "approved"

            elif res.quantity > 0:
                r.status = "partially approved"
                res.quantity = 0

            else:
                r.status = "rejected"
        else:
            r.status = "rejected"

        result.append({
            "request_id": r.id,
            "priority": r.priority,
            "status": r.status
        })

    db.commit()

    return {
        "msg": "allocation done",
        "result": result
    }

