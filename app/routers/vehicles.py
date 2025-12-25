from datetime import date
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.deps import get_db_dep, admin_or_dispatcher, current_user
from app.utils import log_action

router = APIRouter(prefix="/vehicles", tags=["vehicles"], dependencies=[admin_or_dispatcher()])


@router.get("/")
def list_vehicles(db: Session = get_db_dep(), status: models.VehicleStatus | None = None):
    q = db.query(models.Vehicle)
    if status:
        q = q.filter(models.Vehicle.status == status)
    items = q.all()
    today = date.today()
    return [
        {
            "id": v.id,
            "plate": v.plate,
            "status": v.status,
            "model": v.model,
            "warn": any([d and d <= today for d in [v.permit_expire, v.inspection_expire, v.insurance_expire]]),
        }
        for v in items
    ]


@router.post("/")
def create_vehicle(data: schemas.VehicleIn, db: Session = get_db_dep(), user=Depends(current_user)):
    if db.query(models.Vehicle).filter(models.Vehicle.plate == data.plate).first():
        raise HTTPException(400, "Plate exists")
    v = models.Vehicle(**data.model_dump())
    db.add(v)
    db.commit()
    db.refresh(v)
    log_action(db, user.email, user.role.value, "create", "vehicle", v.id, f"create vehicle {v.plate}")
    return v


@router.put("/{vid}")
def update_vehicle(vid: int, data: schemas.VehicleIn, db: Session = get_db_dep(), user=Depends(current_user)):
    v = db.get(models.Vehicle, vid)
    if not v:
        raise HTTPException(404)
    for k, val in data.model_dump().items():
        setattr(v, k, val)
    db.commit()
    db.refresh(v)
    log_action(db, user.email, user.role.value, "update", "vehicle", v.id, f"update vehicle {v.plate}")
    return v


@router.delete("/{vid}")
def delete_vehicle(vid: int, db: Session = get_db_dep(), user=Depends(current_user)):
    v = db.get(models.Vehicle, vid)
    if not v:
        raise HTTPException(404)
    db.delete(v)
    db.commit()
    log_action(db, user.email, user.role.value, "delete", "vehicle", vid, f"delete vehicle {vid}")
    return {"ok": True}
