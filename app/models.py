import enum
from datetime import datetime, date
from sqlalchemy import Column, Integer, String, Date, DateTime, Enum, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base


class Role(str, enum.Enum):
    admin = "admin"
    dispatcher = "dispatcher"
    driver = "driver"


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    role = Column(Enum(Role), nullable=False, default=Role.driver)
    active = Column(Boolean, default=True)


class VehicleStatus(str, enum.Enum):
    available = "available"
    maintenance = "maintenance"
    offline = "offline"


class Vehicle(Base):
    __tablename__ = "vehicles"
    id = Column(Integer, primary_key=True)
    plate = Column(String, unique=True, index=True, nullable=False)
    seats = Column(Integer, nullable=False)
    model = Column(String, nullable=False)
    status = Column(Enum(VehicleStatus), default=VehicleStatus.available)
    permit_expire = Column(Date)
    inspection_expire = Column(Date)
    insurance_expire = Column(Date)
    note = Column(Text)


class StaffStatus(str, enum.Enum):
    on_duty = "on_duty"
    rest = "rest"
    leave = "leave"


class StaffRole(str, enum.Enum):
    driver = "driver"
    attendant = "attendant"
    dispatcher = "dispatcher"


class Staff(Base):
    __tablename__ = "staff"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    role = Column(Enum(StaffRole), nullable=False)
    id_type = Column(String)
    id_expire = Column(Date)
    status = Column(Enum(StaffStatus), default=StaffStatus.on_duty)
    note = Column(Text)


class OrderStatus(str, enum.Enum):
    pending = "pending"
    dispatched = "dispatched"
    in_progress = "in_progress"
    completed = "completed"
    cancelled = "cancelled"


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    customer = Column(String, nullable=False)
    contact = Column(String)
    phone = Column(String)
    ride_time = Column(DateTime, nullable=False)
    origin = Column(String, nullable=False)
    destination = Column(String, nullable=False)
    pax = Column(Integer, nullable=False)
    need_attendant = Column(Boolean, default=False)
    note = Column(Text)
    contract_no = Column(String)
    status = Column(Enum(OrderStatus), default=OrderStatus.pending)


class Dispatch(Base):
    __tablename__ = "dispatches"
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False)
    driver_id = Column(Integer, ForeignKey("staff.id"), nullable=False)
    attendant_id = Column(Integer, ForeignKey("staff.id"))
    trip_code = Column(String, unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    order = relationship("Order")
    vehicle = relationship("Vehicle")
    driver = relationship("Staff", foreign_keys=[driver_id])
    attendant = relationship("Staff", foreign_keys=[attendant_id])
    trip = relationship("Trip", back_populates="dispatch", uselist=False)


class TripStatus(str, enum.Enum):
    assigned = "assigned"
    accepted = "accepted"
    departed = "departed"
    arrived = "arrived"
    finished = "finished"


class Trip(Base):
    __tablename__ = "trips"
    id = Column(Integer, primary_key=True)
    dispatch_id = Column(Integer, ForeignKey("dispatches.id"), nullable=False)
    status = Column(Enum(TripStatus), default=TripStatus.assigned)
    accepted_at = Column(DateTime)
    departed_at = Column(DateTime)
    arrived_at = Column(DateTime)
    finished_at = Column(DateTime)
    receipt_path = Column(String)

    dispatch = relationship("Dispatch", back_populates="trip")


class Log(Base):
    __tablename__ = "logs"
    id = Column(Integer, primary_key=True)
    actor = Column(String)
    role = Column(String)
    action = Column(String)
    target_type = Column(String)
    target_id = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    summary = Column(Text)
