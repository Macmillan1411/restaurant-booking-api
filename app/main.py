from fastapi import FastAPI

from app.routers.table_router import table_router

app = FastAPI(
    title="Restaurant Booking",
    description="API-сервис бронирования столиков в ресторане",
)

app.include_router(table_router, prefix="/tables")
