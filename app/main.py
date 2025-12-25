from fastapi import FastAPI, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from jose import jwt
from app import models
from app.database import engine, Base, get_db
from app.auth import create_access_token, verify_password
from app.config import settings
from app.routers import auth, vehicles, staff, orders, dispatch, trips, exports, logs

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Dispatch MVP", openapi_url="/api/openapi.json", docs_url="/api/docs")

app.include_router(auth.router, prefix="/api")
app.include_router(vehicles.router, prefix="/api")
app.include_router(staff.router, prefix="/api")
app.include_router(orders.router, prefix="/api")
app.include_router(dispatch.router, prefix="/api")
app.include_router(trips.router, prefix="/api")
app.include_router(exports.router, prefix="/api")
app.include_router(logs.router, prefix="/api")

templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/web/login")
def web_login(request: Request, email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        return templates.TemplateResponse("login.html", {"request": request, "error": "bad credentials"}, status_code=400)
    token = create_access_token(user.email, user.role)
    resp = RedirectResponse(url="/dashboard", status_code=302)
    resp.set_cookie(key="token", value=token, httponly=True)
    return resp


def user_from_cookie(request: Request, db: Session):
    token = request.cookies.get("token")
    if not token:
        return None
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])
        email = payload.get("sub")
        return db.query(models.User).filter(models.User.email == email).first()
    except Exception:
        return None


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(get_db)):
    user = user_from_cookie(request, db)
    if not user:
        return RedirectResponse("/", status_code=302)
    return templates.TemplateResponse("dashboard.html", {"request": request, "user": user})
