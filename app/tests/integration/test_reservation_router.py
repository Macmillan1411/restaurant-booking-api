import pytest

from app.schemas.reservation import ReservationRead


@pytest.mark.asyncio
class TestReservationRouter:
    async def test_create_reservation(self, async_client):
        # Create a reservation
        response = await async_client.post(
            "/reservations/",
            json={
                "table_id": 1,
                "customer_name": "John Doe",
                "reservation_time": "2025-04-11T12:00:00",
                "duration_minutes": 60,
            },
        )
        assert response.status_code == 200
        created_reservation = ReservationRead.model_validate(response.json())
        assert created_reservation.table_id == 1
        assert created_reservation.customer_name == "John Doe"
        assert created_reservation.duration_minutes == 60

    async def test_get_all_reservations(self, async_client):
        # Create a reservation first
        await async_client.post(
            "/reservations/",
            json={
                "table_id": 1,
                "customer_name": "Jane Doe",
                "reservation_time": "2025-04-11T14:00:00",
                "duration_minutes": 90,
            },
        )

        # Test get all reservations endpoint
        response = await async_client.get("/reservations/")
        assert response.status_code == 200

        reservations = response.json()
        assert len(reservations) > 0
        assert isinstance(reservations, list)
        assert reservations[1]["customer_name"] == "Jane Doe"

    async def test_delete_reservation(self, async_client):
        # Create a reservation
        create_response = await async_client.post(
            "/reservations/",
            json={
                "table_id": 1,
                "customer_name": "John Smith",
                "reservation_time": "2025-04-11T16:00:00",
                "duration_minutes": 45,
            },
        )
        created_reservation = ReservationRead.model_validate(create_response.json())

        # Delete the reservation
        delete_response = await async_client.delete(
            f"/reservations/{created_reservation.id}"
        )
        assert delete_response.status_code == 200

        # Verify deletion
        get_response = await async_client.get("/reservations/")
        reservations = get_response.json()
        assert not any(
            reservation["id"] == created_reservation.id for reservation in reservations
        )

    async def test_create_reservation_conflict(self, async_client):
        # Create a reservation
        await async_client.post(
            "/reservations/",
            json={
                "table_id": 1,
                "customer_name": "Conflict Test",
                "reservation_time": "2025-04-11T18:00:00",
                "duration_minutes": 60,
            },
        )

        # Attempt to create a conflicting reservation
        response = await async_client.post(
            "/reservations/",
            json={
                "table_id": 1,
                "customer_name": "Conflict Test 2",
                "reservation_time": "2025-04-11T18:30:00",
                "duration_minutes": 60,
            },
        )
        assert response.status_code == 409
        assert "already reserved" in response.json()["detail"].lower()
