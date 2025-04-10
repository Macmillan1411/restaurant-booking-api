from datetime import timedelta

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.core.exceptions import (
    DatabaseOperationException,
    ReservationNotFoundException,
    TableDoesntExistException,
)
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
        """Get all reservations ordered by ID."""
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
            logger.error(f"Database error deleting reservation {id}: {str(e)}")
            raise DatabaseOperationException(
                f"Database error deleting reservation {id}: {str(e)}"
            )

    async def create_reservation(
        self, reservation_data: ReservationCreate, session: AsyncSession
    ):
        """Create a new reservation with conflict management."""
        try:
            # Prepare reservation data
            reservation_data_dict = self._prepare_reservation_data(reservation_data)

            # Check for conflicts
            await self._check_reservation_conflicts(reservation_data, session)

            # Create and save the reservation
            new_reservation = await self._save_reservation(
                reservation_data_dict, session
            )

            logger.info(f"Created reservation for table {reservation_data.table_id}")
            return new_reservation
        except IntegrityError as e:
            logger.error(
                f"Integrity error creating reservation for table {reservation_data.table_id}: {str(e)}"
            )
            raise TableDoesntExistException(
                f"Integrity error creating reservation for table {reservation_data.table_id}"
            )
        except Exception as e:
            logger.error(f"Failed to create reservation: {str(e)}")
            raise

    def _prepare_reservation_data(self, reservation_data: ReservationCreate) -> dict:
        """Prepare reservation data with timezone-naive datetime."""
        reservation_data_dict = reservation_data.model_dump()
        if reservation_data.reservation_time.tzinfo is not None:
            reservation_data_dict["reservation_time"] = (
                reservation_data.reservation_time.replace(tzinfo=None)
            )
        return reservation_data_dict

    async def _check_reservation_conflicts(
        self, reservation_data: ReservationCreate, session: AsyncSession
    ):
        """Check for conflicting reservations."""
        new_start = reservation_data.reservation_time
        new_end = new_start + timedelta(minutes=reservation_data.duration_minutes)

        # Make datetime naive for comparison if needed
        if new_start.tzinfo is not None:
            new_start = new_start.replace(tzinfo=None)
            new_end = new_end.replace(tzinfo=None)

        # Query for overlapping reservations
        statement = select(Reservation).where(
            Reservation.table_id == reservation_data.table_id,
            Reservation.reservation_time < new_end,  # Existing reservation starts before the new one ends
        )
        result = await session.exec(statement)
        existing_reservations = result.all()

        # Extract raw values for conflict checking
        for reservation in existing_reservations:
            existing_start = reservation.reservation_time
            existing_end = existing_start + timedelta(minutes=reservation.duration_minutes)

            if new_start < existing_end and new_end > existing_start:
                logger.warning(
                    f"Reservation conflict detected for table {reservation_data.table_id} "
                    f"from {existing_start} to {existing_end}"
                )
                raise ValueError(
                    f"This table is already reserved from {existing_start} to {existing_end}."
                )

    async def _save_reservation(
        self, reservation_data_dict: dict, session: AsyncSession
    ) -> Reservation:
        """Save the reservation to the database."""
        new_reservation = Reservation(**reservation_data_dict)
        session.add(new_reservation)
        await session.flush()
        await session.refresh(new_reservation)
        return new_reservation
