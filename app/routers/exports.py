import csv
import io
from datetime import date
from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from sqlalchemy import func
from app import models
from app.deps import get_db_dep, admin_or_dispatcher

router = APIRouter(prefix="/export", tags=["export"], dependencies=[admin_or_dispatcher()])


def csv_response(filename: str, rows: list[list[str]]):
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerows(rows)
    return Response(
        buf.getvalue(),
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.get("/orders")
def export_orders(db: Session = get_db_dep(), start: date | None = None, end: date | None = None):
    q = db.query(models.Order)
    if start:
        q = q.filter(func.date(models.Order.ride_time) >= start)
    if end:
        q = q.filter(func.date(models.Order.ride_time) <= end)
    rows = [["id", "customer", "ride_time", "origin", "destination", "status"]]
    for o in q.all():
        rows.append([o.id, o.customer, o.ride_time, o.origin, o.destination, o.status.value])
    return csv_response("orders.csv", rows)


@router.get("/dispatch")
def export_dispatch(db: Session = get_db_dep()):
    rows = [["trip_code", "order", "vehicle", "driver", "created_at"]]
    for d in db.query(models.Dispatch).all():
        rows.append([d.trip_code, d.order_id, d.vehicle.plate, d.driver.name, d.created_at])
    return csv_response("dispatch.csv", rows)


@router.get("/trips")
def export_trips(db: Session = get_db_dep()):
    rows = [["trip_code", "status", "accepted", "departed", "arrived", "finished"]]
    for t in db.query(models.Trip).join(models.Dispatch).all():
        rows.append([t.dispatch.trip_code, t.status.value, t.accepted_at, t.departed_at, t.arrived_at, t.finished_at])
    return csv_response("trips.csv", rows)


@router.get("/vehicle_usage")
def vehicle_usage(db: Session = get_db_dep()):
    rows = [["vehicle", "count"]]
    agg = (
        db.query(models.Vehicle.plate, func.count(models.Dispatch.id))
        .join(models.Dispatch, models.Dispatch.vehicle_id == models.Vehicle.id)
        .group_by(models.Vehicle.plate)
        .all()
    )
    for plate, cnt in agg:
        rows.append([plate, cnt])
    return csv_response("vehicle_usage.csv", rows)


@router.get("/driver_attendance")
def driver_attendance(db: Session = get_db_dep()):
    rows = [["driver", "trips"]]
    agg = (
        db.query(models.Staff.name, func.count(models.Dispatch.id))
        .join(models.Dispatch, models.Dispatch.driver_id == models.Staff.id)
        .group_by(models.Staff.name)
        .all()
    )
    for name, cnt in agg:
        rows.append([name, cnt])
    return csv_response("driver_attendance.csv", rows)
