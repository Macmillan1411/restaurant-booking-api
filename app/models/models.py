from datetime import datetime
from typing import List

from sqlmodel import Field, Relationship, SQLModel


class Table(SQLModel, table=True):
    __tablename__ = "tables"

    id: int | None = Field(default=None, primary_key=True)
    name: str
    seats: int
    location: str

    reservations: List["Reservation"] = Relationship(back_populates="table")


class Reservation(SQLModel, table=True):
    __tablename__ = "reservations"

    id: int | None = Field(default=None, primary_key=True)
    customer_name: str
    table_id: int = Field(foreign_key="tables.id")
    reservation_time: datetime
    duration_minutes: int

    table: Table = Relationship(back_populates="reservations")
