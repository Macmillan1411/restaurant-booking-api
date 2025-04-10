import pytest

from app.schemas.table import TableRead


@pytest.mark.asyncio
class TestTableRouter:
    async def test_create_table(self, async_client):
        response = await async_client.post(
            "/tables/",
            json={"name": "Window Table", "seats": 4, "location": "Main Hall"},
        )
        assert response.status_code == 200
        created_table = TableRead.model_validate(response.json())
        assert created_table.name == "Window Table"
        assert created_table.seats == 4
        assert created_table.location == "Main Hall"

    async def test_get_tables(self, async_client):
        # Create a table first
        await async_client.post(
            "/tables/", json={"name": "Test Table", "seats": 4, "location": "Main Hall"}
        )

        # Test get tables endpoint
        response = await async_client.get("/tables/")
        assert response.status_code == 200

        tables = response.json()
        assert len(tables) > 0
        assert isinstance(tables, list)

    async def test_delete_table(self, async_client):
        # Create table
        create_response = await async_client.post(
            "/tables/", json={"name": "Test Table", "seats": 2, "location": "Corner"}
        )
        created_table = TableRead.model_validate(create_response.json())

        # Delete table
        delete_response = await async_client.delete(f"/tables/{created_table.id}")
        assert delete_response.status_code == 200

        # Verify deletion
        get_response = await async_client.get("/tables/")
        tables = get_response.json()
        assert not any(table["id"] == created_table.id for table in tables)

    async def test_create_table_invalid_data(self, async_client):
        response = await async_client.post(
            "/tables/",
            json={"name": "Invalid Table", "seats": -1, "location": "Main Hall"},
        )
        assert response.status_code == 422
