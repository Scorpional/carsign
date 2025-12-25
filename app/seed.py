from datetime import datetime, timedelta, date
from app.database import SessionLocal
from app import models


def seed():
    db = SessionLocal()
    if db.query(models.Vehicle).count() == 0:
        db.add_all(
            [
                models.Vehicle(
                    plate="ABC123",
                    seats=20,
                    model="Coach",
                    permit_expire=date.today() + timedelta(days=90),
                    inspection_expire=date.today() + timedelta(days=60),
                    insurance_expire=date.today() + timedelta(days=30),
                ),
                models.Vehicle(plate="XYZ789", seats=7, model="MPV"),
            ]
        )
    if db.query(models.Staff).count() == 0:
        db.add_all(
            [
                models.Staff(name="Driver A", phone="driver@example.com", role=models.StaffRole.driver),
                models.Staff(name="Dispatcher A", phone="disp@example.com", role=models.StaffRole.dispatcher),
            ]
        )
    if db.query(models.Order).count() == 0:
        db.add(
            models.Order(
                customer="ACME",
                contact="John",
                phone="123",
                ride_time=datetime.utcnow() + timedelta(days=1),
                origin="Point A",
                destination="Point B",
                pax=10,
            )
        )
    db.commit()
    db.close()
    print("Seeded")


if __name__ == "__main__":
    seed()
