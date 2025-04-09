from datetime import timedelta

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.core.exceptions import DatabaseOperationException, ReservationNotFoundException
from app.core.logger import logger
from app.models.models import Reservation
from app.schemas.reservation import ReservationCreate


class ReservationService:

    async def get_reservation(self, id: int, session: AsyncSession):
        """Get a single reservation by ID."""
        try:
            statement = select(Reservation).where(Reservation.id == id)
            result = await session.exec(statement)
            reservation = result.first()

            if not reservation:
                logger.warning(f"Reservation {id} not found")
                raise ReservationNotFoundException(
                    f"Reservation with id {id} not found"
                )

            logger.info(f"Retrieved reservation {id}")
            return reservation
        except SQLAlchemyError as e:
            logger.error(f"Database error fetching reservation {id}: {str(e)}")
            raise DatabaseOperationException(
                f"Database error retrieving reservation {id}"
            )

    async def get_all_reservations(self, session: AsyncSession):
        """Get all reservation ordered by ID."""
        statement = select(Reservation).order_by(Reservation.id)
        try:
            result = await session.exec(statement)
        except SQLAlchemyError as e:
            logger.error(f"Database error retrieving all reservations: {str(e)}")
            raise DatabaseOperationException(
                f"Database error retrieving all reservations: {str(e)}"
            )

        return result.all()

    async def delete_reservation(self, id: int, session: AsyncSession):
        """Delete a reservation by ID."""
        reservation_to_delete = await self.get_reservation(id, session)

        try:
            await session.delete(reservation_to_delete)
            await session.flush()
        except SQLAlchemyError as e:
            logger.error(f"Database error deleting table {id}: {str(e)}")
            raise DatabaseOperationException(
                f"Database error deleting table {id}: {str(e)}"
            )

    async def create_reservation(
        self, reservation_data: ReservationCreate, session: AsyncSession
    ):
        """create a new reservation with conflict management"""
        try:
            # Handle timezone for new reservation
            if reservation_data.reservation_time.tzinfo is not None:
                # Store a copy of reservation_data with timezone-naive datetime
                # This is critical for databases that store WITHOUT TIME ZONE
                reservation_data_dict = reservation_data.model_dump()
                reservation_data_dict["reservation_time"] = (
                    reservation_data.reservation_time.replace(tzinfo=None)
                )
            else:
                reservation_data_dict = reservation_data.model_dump()

            # Calculate time range for conflict checking
            new_start = reservation_data.reservation_time
            new_end = new_start + timedelta(minutes=reservation_data.duration_minutes)

            # Also make these naive for comparison if needed
            if new_start.tzinfo is not None:
                new_start = new_start.replace(tzinfo=None)
                new_end = new_end.replace(tzinfo=None)

            # Query using simple time-based filtering
            statement = (
                select(Reservation)
                .where(
                    Reservation.table_id == reservation_data.table_id,
                    Reservation.reservation_time <= new_end,
                )
                .limit(10)
            )

            result = await session.exec(statement)
            existing_reservations = result.all()

            for reservation in existing_reservations:
                existing_start = reservation.reservation_time
                existing_end = existing_start + timedelta(
                    minutes=reservation.duration_minutes
                )

                if new_start < existing_end and new_end > existing_start:
                    logger.warning(
                        f"Reservation conflict detected for table {reservation_data.table_id}"
                    )
                    raise ValueError(
                        "This table is already reserved during the requested time slot"
                    )

            # Create new reservation with timezone-naive datetime
            new_reservation = Reservation(**reservation_data_dict)
            session.add(new_reservation)
            await session.flush()
            await session.refresh(new_reservation)

            logger.info(f"Created reservation for table {reservation_data.table_id}")
            return new_reservation
        except Exception as e:
            logger.error(f"Failed to create reservation: {str(e)}")
            raise
