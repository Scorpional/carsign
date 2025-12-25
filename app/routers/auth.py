from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import models, schemas
from app.auth import verify_password, hash_password, create_access_token
from app.database import get_db
from app.utils import log_action

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect credentials")
    token = create_access_token(user.email, user.role)
    log_action(db, user.email, user.role.value, "login", "user", user.id, "user login")
    return {"access_token": token}


@router.post("/register", response_model=schemas.UserOut)
def register(data: schemas.UserCreate, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.email == data.email).first():
        raise HTTPException(400, "Email exists")
    user = models.User(email=data.email, full_name=data.full_name, role=data.role, hashed_password=hash_password(data.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    log_action(db, data.email, data.role.value, "register", "user", user.id, "user registered")
    return user
