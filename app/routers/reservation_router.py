from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.core.exceptions import DatabaseOperationException, ReservationNotFoundException
from app.schemas.reservation import ReservationCreate, ReservationRead
from app.services.reservation_service import ReservationService

reservation_router = APIRouter()
reservation_service = ReservationService()


@reservation_router.get("/", response_model=List[ReservationRead])
async def get_all_reservations(session: AsyncSession = Depends(get_session)):
    try:
        reservations = await reservation_service.get_all_reservations(session)
    except DatabaseOperationException as e:
        raise HTTPException(status_code=500, detail=str(e))
    return reservations


@reservation_router.post("/", response_model=ReservationRead)
async def create_reservation(
    reservation_data: ReservationCreate, session: AsyncSession = Depends(get_session)
):
    """Create a reservation"""
    try:
        new_reservation = await reservation_service.create_reservation(
            reservation_data, session
        )
    except DatabaseOperationException as e:
        raise HTTPException(status_code=500, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))
    return new_reservation


@reservation_router.delete("/", status_code=status.HTTP_200_OK)
async def delete_reservation(id: int, session: AsyncSession = Depends(get_session)):
    """Delete a reservation by id"""
    try:
        result = await reservation_service.delete_reservation(id, session)
    except ReservationNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except DatabaseOperationException as e:
        raise HTTPException(status_code=500, detail=str(e))
    return result
