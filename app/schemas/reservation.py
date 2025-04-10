from datetime import datetime

from pydantic import BaseModel


class ReservationCreate(BaseModel):
    customer_name: str
    table_id: int
    reservation_time: datetime
    duration_minutes: int


class ReservationRead(BaseModel):
    id: int
    customer_name: str
    table_id: int
    reservation_time: datetime
    duration_minutes: int

    class Config:
        from_attributes = True
