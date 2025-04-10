import pytest

from app.core.exceptions import ReservationNotFoundException


@pytest.mark.asyncio
class TestReservationService:
    async def test_get_reservation_success(
        self, reservation_service, mock_reservation, mock_session
    ):
        session, result = mock_session
        result.first.return_value = mock_reservation

        result = await reservation_service.get_reservation(1, session)

        assert result.id == mock_reservation.id
        assert result.table_id == mock_reservation.table_id
        assert result.customer_name == mock_reservation.customer_name
        assert result.duration_minutes == mock_reservation.duration_minutes
        session.exec.assert_called_once()

    async def test_get_reservation_not_found(self, reservation_service, mock_session):
        session, result = mock_session
        result.first.return_value = None

        with pytest.raises(ReservationNotFoundException) as exc_info:
            await reservation_service.get_reservation(1, session)

        assert "Reservation with id 1 not found" in str(exc_info.value)
        session.exec.assert_called_once()

    async def test_create_reservation_success(
        self, reservation_service, sample_reservation_data, mock_session
    ):
        session, result = mock_session
        result.all.return_value = []  # No conflicts
        session.refresh.side_effect = lambda x: setattr(x, "id", 1)

        result = await reservation_service.create_reservation(
            sample_reservation_data, session
        )

        assert result.id == 1
        assert result.table_id == sample_reservation_data.table_id
        assert result.customer_name == sample_reservation_data.customer_name
        assert result.duration_minutes == sample_reservation_data.duration_minutes
        session.add.assert_called_once()
        session.flush.assert_called_once()
        session.refresh.assert_called_once()

    async def test_create_reservation_conflict(
        self,
        reservation_service,
        sample_reservation_data,
        mock_reservation,
        mock_session,
    ):
        session, result = mock_session
        result.all.return_value = [mock_reservation]  # Existing reservation

        with pytest.raises(ValueError) as exc_info:
            await reservation_service.create_reservation(
                sample_reservation_data, session
            )

        assert "table is already reserved" in str(exc_info.value).lower()
        session.add.assert_not_called()

    async def test_get_all_reservations_success(
        self, reservation_service, mock_reservation, mock_session
    ):
        session, result = mock_session
        result.all.return_value = [mock_reservation]

        result = await reservation_service.get_all_reservations(session)

        assert len(result) == 1
        assert result[0].id == mock_reservation.id
        assert result[0].table_id == mock_reservation.table_id
        session.exec.assert_called_once()

    async def test_delete_reservation_success(
        self, reservation_service, mock_reservation, mock_session
    ):
        session, result = mock_session
        result.first.return_value = mock_reservation

        await reservation_service.delete_reservation(1, session)

        session.delete.assert_called_once()
        session.flush.assert_called_once()

    async def test_delete_reservation_not_found(
        self, reservation_service, mock_session
    ):
        session, result = mock_session
        result.first.return_value = None

        with pytest.raises(ReservationNotFoundException):
            await reservation_service.delete_reservation(1, session)

        session.delete.assert_not_called()
