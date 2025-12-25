from fastapi import APIRouter
from sqlalchemy.orm import Session
from app import models
from app.deps import get_db_dep, admin_or_dispatcher

router = APIRouter(prefix="/logs", tags=["logs"], dependencies=[admin_or_dispatcher()])


@router.get("/")
def list_logs(db: Session = get_db_dep()):
    return db.query(models.Log).order_by(models.Log.created_at.desc()).limit(200).all()
