from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.core.exceptions import DatabaseOperationException, TableNotFoundException
from app.models.models import Table
from app.schemas.table import TableCreate
from app.core.logger import logger


class TableService:
    async def get_table(self, id: int, session: AsyncSession):
        """Get a single table by ID."""
        try:
            statement = select(Table).where(Table.id == id)
            result = await session.exec(statement)
            table = result.first()

            if not table:
                logger.warning(f"Table with id {id} not found")
                raise TableNotFoundException(f"Table with id {id} not found")

            return table
        except SQLAlchemyError as e:
            logger.error(f"Database error retrieving table {id}: {str(e)}")
            raise DatabaseOperationException(
                f"Database error retrieving table {id}: {str(e)}"
            )
        except TableNotFoundException:
            raise

    async def create_table(self, table_data: TableCreate, session: AsyncSession):
        """Create a new table."""
        try:
            table_data_dict = table_data.model_dump()
            new_table = Table(**table_data_dict)

            session.add(new_table)
            await session.flush()
            await session.refresh(new_table)
            logger.info(f"Table with id {new_table.id} successfully created.")
            return new_table
        except SQLAlchemyError as e:
            logger.error(f"Database error creating table: {str(e)}")
            raise DatabaseOperationException(f"Database error creating table: {str(e)}")

    async def get_all_tables(self, session: AsyncSession):
        """Get all tables ordered by ID."""
        try:
            statement = select(Table).order_by(Table.id)
            result = await session.exec(statement)
            return result.all()
        except SQLAlchemyError as e:
            logger.error(f"Database error retrieving all tables: {str(e)}")
            raise DatabaseOperationException(
                f"Database error retrieving all tables: {str(e)}"
            )

    async def delete_table(self, id: int, session: AsyncSession):
        """Delete a table by ID."""
        table_to_delete = await self.get_table(id, session)

        try:
            await session.delete(table_to_delete)
            await session.flush()
        except SQLAlchemyError as e:
            logger.error(f"Database error deleting table {id}: {str(e)}")
            raise DatabaseOperationException(
                f"Database error deleting table {id}: {str(e)}"
            )

    async def update_table(
        self, id: int, table_data: TableCreate, session: AsyncSession
    ):
        """Update a table by ID."""
        table_to_update = await self.get_table(id, session)

        try:
            update_data = table_data.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(table_to_update, key, value)

            await session.flush()
            await session.refresh(table_to_update)
            logger.info(f"Table with id {id} has been successfully updated")
            return table_to_update
        except SQLAlchemyError as e:
            logger.error( f"Database error updating table {id}: {str(e)}")
            raise DatabaseOperationException(
                f"Database error updating table {id}: {str(e)}"
            )
