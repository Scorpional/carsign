from datetime import datetime
import os
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.deps import get_db_dep, driver_only, current_user
from app.config import settings
from app.utils import log_action

router = APIRouter(prefix="/trips", tags=["trips"])


@router.get("/mine", dependencies=[driver_only()])
def my_trips(db: Session = get_db_dep(), user=Depends(current_user)):
    staff = db.query(models.Staff).filter(models.Staff.phone == user.email).first()
    driver_id = staff.id if staff else -1
    q = db.query(models.Trip).join(models.Dispatch).filter(models.Dispatch.driver_id == driver_id)
    return q.all()


@router.post("/{tid}/status", dependencies=[driver_only()])
def update_status(tid: int, data: schemas.TripUpdate, db: Session = get_db_dep(), user=Depends(current_user)):
    t = db.get(models.Trip, tid)
    if not t:
        raise HTTPException(404)
    now = datetime.utcnow()
    t.status = data.status
    if data.status == models.TripStatus.accepted:
        t.accepted_at = now
    if data.status == models.TripStatus.departed:
        t.departed_at = now
    if data.status == models.TripStatus.arrived:
        t.arrived_at = now
    if data.status == models.TripStatus.finished:
        t.finished_at = now
    db.commit()
    db.refresh(t)
    log_action(db, user.email, user.role.value, "trip_status", "trip", t.id, f"status {t.status.value}")
    return t


@router.post("/{tid}/upload", dependencies=[driver_only()])
def upload_receipt(tid: int, file: UploadFile = File(...), db: Session = get_db_dep(), user=Depends(current_user)):
    if file.content_type not in ["image/png", "image/jpeg", "application/pdf"]:
        raise HTTPException(400, "Invalid file type")
    contents = file.file.read()
    if len(contents) > 10 * 1024 * 1024:
        raise HTTPException(400, "File too large")
    os.makedirs(settings.upload_dir, exist_ok=True)
    path = os.path.join(settings.upload_dir, f"trip_{tid}_{file.filename}")
    with open(path, "wb") as f:
        f.write(contents)
    t = db.get(models.Trip, tid)
    if not t:
        raise HTTPException(404)
    t.receipt_path = path
    db.commit()
    log_action(db, user.email, user.role.value, "upload_receipt", "trip", tid, path)
    return {"path": path}
