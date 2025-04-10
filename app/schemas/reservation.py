from datetime import datetime, timedelta
from pydantic import BaseModel, Field


class ReservationCreate(BaseModel):
    customer_name: str = Field(
        min_length=2,
        max_length=50,
    )
    table_id: int = Field(
        gt=0,
    )
    reservation_time: datetime = Field(
        gt=datetime.now(),
        lt=datetime.now() + timedelta(days=30),
    )
    duration_minutes: int = Field(
        gt=10,
        le=240,  # 4 hours maximum
    )


class ReservationRead(BaseModel):
    id: int
    customer_name: str
    table_id: int
    reservation_time: datetime
    duration_minutes: int

    class Config:
        from_attributes = True
