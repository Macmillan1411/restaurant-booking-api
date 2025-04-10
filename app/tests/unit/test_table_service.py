import pytest

from app.core.exceptions import TableNotFoundException


@pytest.mark.asyncio
class TestTableService:
    async def test_get_table_success(self, table_service, mock_table, mock_session):
        session, result = mock_session
        result.first.return_value = mock_table

        result = await table_service.get_table(1, session)

        assert result.id == mock_table.id
        assert result.name == mock_table.name
        assert result.seats == mock_table.seats
        assert result.location == mock_table.location
        session.exec.assert_called_once()

    async def test_get_table_not_found(self, table_service, mock_session):
        session, result = mock_session
        result.first.return_value = None

        with pytest.raises(TableNotFoundException) as exc_info:
            await table_service.get_table(1, session)

        assert "Table with id 1 not found" in str(exc_info.value)
        session.exec.assert_called_once()

    async def test_get_all_tables_success(
        self, table_service, mock_tables, mock_session
    ):
        session, result = mock_session
        result.all.return_value = mock_tables

        result = await table_service.get_all_tables(session)

        assert len(result) == 3
        assert result[0].name == mock_tables[0].name
        assert result[1].seats == mock_tables[1].seats
        assert result[2].location == mock_tables[2].location
        session.exec.assert_called_once()

    async def test_create_table_success(
        self, table_service, table_create_data, mock_session
    ):
        session, _ = mock_session
        session.refresh.side_effect = lambda x: setattr(x, "id", 1)

        result = await table_service.create_table(table_create_data, session)

        assert result.id == 1
        assert result.name == table_create_data.name
        assert result.seats == table_create_data.seats
        assert result.location == table_create_data.location
        session.add.assert_called_once()
        session.flush.assert_called_once()
        session.refresh.assert_called_once()

    async def test_delete_table_success(self, table_service, mock_table, mock_session):
        session, result = mock_session
        result.first.return_value = mock_table

        await table_service.delete_table(1, session)

        session.delete.assert_called_once_with(mock_table)
        session.flush.assert_called_once()
