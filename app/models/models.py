from datetime import datetime

from sqlmodel import Field, Relationship, SQLModel


class Table(SQLModel, table=True):
    __tablename__ = "tables"

    id: int | None = Field(default=None, primary_key=True)
    name: str
    seats: int
    location: str

    reservations: list["Reservation"] = Relationship(back_populates="tables")


class Reservation(SQLModel, table=True):
    __tablename__ = "reservations"

    id: int | None = Field(default=None, primary_key=True)
    customer_name: str
    table_id: int = Field(foreign_key="tables.id")
    reservation_time: datetime
    duration_minutes: int

    table: Table = Relationship(back_populates="reservations")
