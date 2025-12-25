from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel, EmailStr
from app.models import Role, VehicleStatus, StaffRole, StaffStatus, OrderStatus, TripStatus


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: str
    role: Role


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    role: Role


class UserOut(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    role: Role

    class Config:
        from_attributes = True


class VehicleIn(BaseModel):
    plate: str
    seats: int
    model: str
    status: VehicleStatus
    permit_expire: Optional[date]
    inspection_expire: Optional[date]
    insurance_expire: Optional[date]
    note: Optional[str]


class StaffIn(BaseModel):
    name: str
    phone: str
    role: StaffRole
    id_type: Optional[str]
    id_expire: Optional[date]
    status: StaffStatus
    note: Optional[str]


class OrderIn(BaseModel):
    customer: str
    contact: Optional[str]
    phone: Optional[str]
    ride_time: datetime
    origin: str
    destination: str
    pax: int
    need_attendant: bool = False
    note: Optional[str]
    contract_no: Optional[str]
    status: OrderStatus = OrderStatus.pending


class DispatchIn(BaseModel):
    order_id: int
    vehicle_id: int
    driver_id: int
    attendant_id: Optional[int]


class TripUpdate(BaseModel):
    status: TripStatus
