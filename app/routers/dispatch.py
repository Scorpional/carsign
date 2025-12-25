from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app import models, schemas, utils
from app.deps import get_db_dep, admin_or_dispatcher, current_user
from app.utils import log_action

router = APIRouter(prefix="/dispatch", tags=["dispatch"], dependencies=[admin_or_dispatcher()])


def has_conflict(db: Session, vehicle_id: int, driver_id: int, ride_time):
    conflict = (
        db.query(models.Dispatch)
        .join(models.Order)
        .filter(
            and_(
                models.Order.ride_time == ride_time,
                (models.Dispatch.vehicle_id == vehicle_id) | (models.Dispatch.driver_id == driver_id),
            )
        )
        .first()
    )
    return conflict is not None


@router.post("/")
def create_dispatch(data: schemas.DispatchIn, db: Session = get_db_dep(), user=Depends(current_user)):
    order = db.get(models.Order, data.order_id)
    if not order:
        raise HTTPException(404, "Order missing")
    if has_conflict(db, data.vehicle_id, data.driver_id, order.ride_time):
        raise HTTPException(400, "Conflict vehicle/driver")
    count = db.query(models.Dispatch).count()
    code = utils.generate_trip_code(count)
    d = models.Dispatch(
        order_id=data.order_id,
        vehicle_id=data.vehicle_id,
        driver_id=data.driver_id,
        attendant_id=data.attendant_id,
        trip_code=code,
    )
    db.add(d)
    db.flush()
    t = models.Trip(dispatch=d)
    order.status = models.OrderStatus.dispatched
    db.add(t)
    db.commit()
    db.refresh(d)
    log_action(db, user.email, user.role.value, "dispatch", "dispatch", d.id, f"dispatch {code}")
    return d


@router.get("/")
def list_dispatches(db: Session = get_db_dep()):
    return db.query(models.Dispatch).all()


@router.get("/{did}/print")
def print_dispatch(did: int, db: Session = get_db_dep()):
    d = db.get(models.Dispatch, did)
    if not d:
        raise HTTPException(404)
    return {
        "header": "Company Dispatch Sheet",
        "trip_code": d.trip_code,
        "date": datetime.utcnow().date(),
        "vehicle": d.vehicle.plate,
        "driver": d.driver.name,
        "order": {"origin": d.order.origin, "destination": d.order.destination, "time": d.order.ride_time},
    }
