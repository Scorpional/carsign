from fastapi import Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import get_current_user, require_roles
from app import models


def get_db_dep():
    return Depends(get_db)


def current_user():
    return Depends(get_current_user)


def admin_or_dispatcher():
    return Depends(require_roles(models.Role.admin, models.Role.dispatcher))


def driver_only():
    return Depends(require_roles(models.Role.driver))
