from datetime import datetime
from sqlalchemy.orm import Session
from app import models


def generate_trip_code(db_count: int) -> str:
    today = datetime.utcnow().strftime("%Y%m%d")
    return f"{today}-{db_count+1:04d}"


def log_action(db: Session, actor: str, role: str, action: str, target_type: str, target_id: int | None, summary: str):
    entry = models.Log(
        actor=actor,
        role=role,
        action=action,
        target_type=target_type,
        target_id=target_id,
        summary=summary,
    )
    db.add(entry)
    db.commit()
