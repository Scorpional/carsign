from app.config import settings
from app.database import SessionLocal
from app import models
from app.auth import hash_password


def main():
    db = SessionLocal()
    user = db.query(models.User).filter(models.User.email == settings.admin_email).first()
    if not user:
        admin = models.User(
            email=settings.admin_email,
            full_name="Admin",
            role=models.Role.admin,
            hashed_password=hash_password(settings.admin_password),
            active=True,
        )
        db.add(admin)
        db.commit()
        print("Admin created")
    db.close()


if __name__ == "__main__":
    main()
