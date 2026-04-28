from fastapi.responses import RedirectResponse
from fastapi import APIRouter, Depends, Form, Request
from sqlalchemy.orm import Session
from database import SessionLocal
import models
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")


# ---------------- DATABASE ----------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------- SESSION SHORTCUTS ----------------
def get_user(request: Request):
    return request.session.get("user_id")

def get_role(request: Request):
    return request.session.get("role")


# ---------------- LOGIN & REGISTER PAGES ----------------
@router.get("/login-page")
def login_page(request: Request):
    return templates.TemplateResponse(
        request,
        "login.html",
        {"request": request}
    )


@router.get("/register-page")
def register_page(request: Request):
    return templates.TemplateResponse(
        request,
        "register.html",
        {"request": request}
    )


# ---------------- SUBMIT REQUEST ----------------
@router.post("/submit-request")
def create_request(
    request: Request,
    resource_id: int = Form(...),
    quantity: int = Form(...),
    priority: str = Form(...),
    db: Session = Depends(get_db)
):
    user_id = get_user(request)

    if not user_id:
        request.session["next"] = "/resource-page"
        return RedirectResponse("/login-page", status_code=302)

    req = models.Request(
        user_id=user_id,
        resource_id=resource_id,
        quantity=quantity,
        priority=priority,
        status="pending",
        verified=False
    )

    db.add(req)
    db.commit()

    return templates.TemplateResponse(
        request,
        "resource.html",
        {"request": request, "success": True}
    )


# ---------------- RESOURCE PAGE ----------------
@router.get("/resource-page")
def resource_page(request: Request):
    if not get_user(request):
        request.session["next"] = "/resource-page"
        return RedirectResponse("/login-page", status_code=302)

    return templates.TemplateResponse(
        request,
        "resource.html",
        {"request": request}
    )


# ---------------- ALLOCATION (ADMIN ONLY) ----------------
@router.get("/allocation")
def allocation_page(request: Request):
    if get_role(request) != "admin":
        request.session["next"] = "/allocation"
        return RedirectResponse("/login-page", status_code=302)

    return templates.TemplateResponse(
        request,
        "allocation.html",
        {"request": request}
    )


@router.post("/allocate")
async def allocate_resource(request: Request, db: Session = Depends(get_db)):
    if get_role(request) != "admin":
        return RedirectResponse("/login-page", status_code=302)

    form = await request.form()

    resource_id = int(form.get("resource_id"))
    quantity = int(form.get("quantity"))

    resource = db.query(models.Resource).filter(
        models.Resource.id == resource_id
    ).first()

    if not resource:
        return templates.TemplateResponse(
            request,
            "allocation.html",
            {"request": request, "error": "❌ Resource not found"}
        )

    if resource.quantity < quantity:
        return templates.TemplateResponse(
            request,
            "allocation.html",
            {"request": request, "error": "❌ Not enough stock"}
        )

    # ✅ FIXED HERE
    pending_requests = db.query(models.Request).filter(
        models.Request.resource_id == resource_id,
        models.Request.status == "pending",
        models.Request.verified == True
    ).all()

    remaining = quantity

    for req in pending_requests:
        if remaining >= req.quantity:
            remaining -= req.quantity
            req.status = "successful"
        else:
            break

    resource.quantity -= quantity
    db.commit()

    return templates.TemplateResponse(
        request,
        "allocation.html",
        {"request": request, "message": "✅ Allocation completed"}
    )


# ---------------- REPORT DISASTER ----------------
@router.post("/submit-report")
def submit_report(
    request: Request,
    location: str = Form(...),
    disaster_type: str = Form(...),
    severity: str = Form(...),
    db: Session = Depends(get_db)
):
    if not get_user(request):
        request.session["next"] = "/report-page"
        return RedirectResponse("/login-page", status_code=302)

    disaster = models.Disaster(
        location=location,
        type=disaster_type,
        severity=severity
    )

    db.add(disaster)
    db.commit()

    return templates.TemplateResponse(
        request,
        "report.html",
        {"request": request, "success": True}
    )


# ---------------- REPORT PAGE ----------------
@router.get("/report-page")
def report_page(request: Request):
    if not get_user(request):
        request.session["next"] = "/report-page"
        return RedirectResponse("/login-page", status_code=302)

    return templates.TemplateResponse(
        request,
        "report.html",
        {"request": request}
    )


# ---------------- REPORTS PAGE ----------------
@router.get("/reports-page")
def reports_page(request: Request, db: Session = Depends(get_db)):
    user_id = get_user(request)
    role = get_role(request)

    if not user_id:
        return RedirectResponse("/login-page", status_code=302)

    if role == "admin":
        requests = db.query(models.Request).all()

    elif role == "volunteer":
        requests = db.query(models.Request).filter(
            models.Request.status == "pending"
        ).all()

    else:
        requests = db.query(models.Request).filter(
            models.Request.user_id == user_id
        ).all()

    return templates.TemplateResponse(
        request,
        "reports.html",
        {"request": request, "requests": requests}
    )


# ---------------- VOLUNTEER ----------------
@router.post("/add-volunteer")
def register_volunteer(
    name: str = Form(...),
    skill: str = Form(...),
    db: Session = Depends(get_db)
):
    volunteer = models.Volunteer(
        name=name,
        skill=skill,
        status="available"
    )

    db.add(volunteer)
    db.commit()

    return RedirectResponse("/volunteer-page", status_code=302)


# ---------------- ADMIN REQUESTS ----------------
@router.get("/admin-requests")
def admin_requests(request: Request, db: Session = Depends(get_db)):
    if get_role(request) != "admin":
        return RedirectResponse("/login-page", status_code=302)

    requests = db.query(models.Request).all()

    return templates.TemplateResponse(
        request,
        "admin_requests.html",
        {"request": request, "requests": requests}
    )


# ---------------- VERIFY REQUEST ----------------
@router.post("/verify/{req_id}")
def verify_request(req_id: int, request: Request, db: Session = Depends(get_db)):

    if get_role(request) != "volunteer":
        return RedirectResponse("/login-page", status_code=302)

    req = db.query(models.Request).filter(models.Request.id == req_id).first()

    if req:
        req.verified = True
        db.commit()

    return RedirectResponse("/reports-page", status_code=302)


# ---------------- LOGOUT ----------------
@router.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/", status_code=302)