from datetime import date
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.deps import get_db_dep, admin_or_dispatcher, current_user
from app.utils import log_action

router = APIRouter(prefix="/staff", tags=["staff"], dependencies=[admin_or_dispatcher()])


@router.get("/")
def list_staff(db: Session = get_db_dep(), role: models.StaffRole | None = None):
    q = db.query(models.Staff)
    if role:
        q = q.filter(models.Staff.role == role)
    today = date.today()
    return [{"id": s.id, "name": s.name, "role": s.role, "phone": s.phone, "warn": s.id_expire and s.id_expire <= today} for s in q.all()]


@router.post("/")
def create_staff(data: schemas.StaffIn, db: Session = get_db_dep(), user=Depends(current_user)):
    s = models.Staff(**data.model_dump())
    db.add(s)
    db.commit()
    db.refresh(s)
    log_action(db, user.email, user.role.value, "create", "staff", s.id, f"create staff {s.name}")
    return s


@router.put("/{sid}")
def update_staff(sid: int, data: schemas.StaffIn, db: Session = get_db_dep(), user=Depends(current_user)):
    s = db.get(models.Staff, sid)
    if not s:
        raise HTTPException(404)
    for k, v in data.model_dump().items():
        setattr(s, k, v)
    db.commit()
    db.refresh(s)
    log_action(db, user.email, user.role.value, "update", "staff", s.id, f"update staff {s.name}")
    return s


@router.delete("/{sid}")
def delete_staff(sid: int, db: Session = get_db_dep(), user=Depends(current_user)):
    s = db.get(models.Staff, sid)
    if not s:
        raise HTTPException(404)
    db.delete(s)
    db.commit()
    log_action(db, user.email, user.role.value, "delete", "staff", sid, f"delete staff {sid}")
    return {"ok": True}
