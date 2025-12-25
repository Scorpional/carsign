from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.deps import get_db_dep, admin_or_dispatcher, current_user
from app.utils import log_action

router = APIRouter(prefix="/orders", tags=["orders"], dependencies=[admin_or_dispatcher()])


@router.get("/")
def list_orders(db: Session = get_db_dep(), q: str | None = None):
    query = db.query(models.Order)
    if q:
        like = f"%{q}%"
        query = query.filter(models.Order.customer.ilike(like))
    return query.order_by(models.Order.ride_time.desc()).all()


@router.post("/")
def create_order(data: schemas.OrderIn, db: Session = get_db_dep(), user=Depends(current_user)):
    o = models.Order(**data.model_dump())
    db.add(o)
    db.commit()
    db.refresh(o)
    log_action(db, user.email, user.role.value, "create", "order", o.id, f"create order {o.customer}")
    return o


@router.put("/{oid}")
def update_order(oid: int, data: schemas.OrderIn, db: Session = get_db_dep(), user=Depends(current_user)):
    o = db.get(models.Order, oid)
    if not o:
        raise HTTPException(404)
    for k, v in data.model_dump().items():
        setattr(o, k, v)
    db.commit()
    db.refresh(o)
    log_action(db, user.email, user.role.value, "update", "order", o.id, f"update order {o.customer}")
    return o


@router.delete("/{oid}")
def delete_order(oid: int, db: Session = get_db_dep(), user=Depends(current_user)):
    o = db.get(models.Order, oid)
    if not o:
        raise HTTPException(404)
    db.delete(o)
    db.commit()
    log_action(db, user.email, user.role.value, "delete", "order", oid, f"delete order {oid}")
    return {"ok": True}
