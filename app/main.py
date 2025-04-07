from fastapi import FastAPI

version = 'v1'

app = FastAPI(
    title="Restaurant Booking",
    description="API-сервис бронирования столиков в ресторане",
    version=version,
)


@app.get('/greet')
async def method_name():
    return  {"message": "Hello World!"}