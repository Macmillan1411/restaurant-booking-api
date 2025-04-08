from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.core.exceptions import DatabaseOperationException, TableNotFoundException
from app.schemas.table import TableCreate, TableRead
from app.services.table_service import TableService

table_router = APIRouter()
table_service = TableService()


@table_router.get("/", response_model=List[TableRead])
async def get_all_tables(session: AsyncSession = Depends(get_session)):
    """List all tables"""
    try:
        tables = await table_service.get_all_tables(session)
    except DatabaseOperationException as e:
        raise HTTPException(status_code=500, detail=str(e))
    return tables


@table_router.post("/", response_model=TableRead)
async def create_table(
    table_data: TableCreate, session: AsyncSession = Depends(get_session)
):
    """Create a table"""
    try:
        new_table = await table_service.create_table(table_data, session)
    except DatabaseOperationException as e:
        raise HTTPException(status_code=500, detail=str(e))

    return new_table


@table_router.delete("/", status_code=status.HTTP_200_OK)
async def delete_table(id: int, session: AsyncSession = Depends(get_session)):
    """Delete a table by id"""
    try:
        result = await table_service.delete_table(id, session)
    except TableNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except DatabaseOperationException as e:
        raise HTTPException(status_code=500, detail=str(e))

    return result
