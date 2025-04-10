import os
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, Mock

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession  # Use this AsyncSession

from app.core.database import get_session  # Import the database dependency
from app.main import app
from app.models.models import Reservation, Table
from app.schemas.reservation import ReservationCreate
from app.schemas.table import TableCreate
from app.services.reservation_service import ReservationService
from app.services.table_service import TableService

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Set the environment variable for the test database
os.environ["DATABASE_URL"] = TEST_DATABASE_URL


# Unit test fixtures
@pytest.fixture
def mock_session():
    session = AsyncMock()
    mock_result = Mock()
    session.exec.return_value = mock_result
    return session, mock_result


@pytest.fixture
def table_service():
    return TableService()


@pytest.fixture
def reservation_service():
    return ReservationService()


@pytest.fixture
def mock_table():
    return Table(id=1, name="Test Table", seats=4, location="Main Hall")


@pytest.fixture
def mock_tables():
    return [
        Table(id=1, name="Table 1", seats=4, location="Main Hall"),
        Table(id=2, name="Table 2", seats=2, location="Window"),
        Table(id=3, name="Table 3", seats=6, location="Outdoor"),
    ]


@pytest.fixture
def table_create_data():
    return TableCreate(name="New Table", seats=4, location="Main Hall")


@pytest.fixture
def mock_reservation():
    return Reservation(
        id=1,
        table_id=1,
        customer_name="John Doe",
        reservation_time=datetime.now() + timedelta(days=1),
        duration_minutes=60,
    )


@pytest.fixture
def sample_reservation_data():
    return ReservationCreate(
        table_id=1,
        customer_name="John Doe",
        reservation_time=datetime.now() + timedelta(days=1),
        duration_minutes=60,
    )


# Integration test fixtures
@pytest_asyncio.fixture(scope="session")
async def test_engine():
    engine = create_async_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)

    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)


@pytest.fixture
async def test_session(test_engine) -> AsyncSession:
    async_session = sessionmaker(
        test_engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session() as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def override_get_db(test_engine):
    """Override the get_db dependency to use the test engine."""

    async def _get_test_db():
        async_session = sessionmaker(
            test_engine, class_=AsyncSession, expire_on_commit=False
        )
        async with async_session() as session:
            yield session
            await session.commit()

    app.dependency_overrides[get_session] = _get_test_db


@pytest_asyncio.fixture
async def async_client():
    """Async client for testing the FastAPI app."""
    client = AsyncClient(transport=ASGITransport(app=app), base_url="http://127.0.0.1")
    yield client
    await client.aclose()
