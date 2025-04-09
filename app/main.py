from fastapi import FastAPI, Request
from app.core.logger import logger
import time

from app.routers.reservation_router import reservation_router
from app.routers.table_router import table_router

app = FastAPI(
    title="Restaurant Booking",
    description="API-сервис бронирования столиков в ресторане",
)

app.include_router(table_router, prefix="/tables", tags=["tables"])
app.include_router(reservation_router, prefix="/reservations", tags=["reservations"])

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000

    logger.info(
        f"[{request.method}] {request.url.path} - {response.status_code} - {process_time:.2f}ms"
    )
    return response
