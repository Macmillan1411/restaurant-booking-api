# Restaurant Booking API

A simple REST API service for restaurant table booking management built with FastAPI and PostgreSQL.

## Features

- Manage restaurant tables (create, list, delete)
- Handle table reservations with time conflict detection

## Requirements

- Docker

## Quick Start

1. Clone the repository:
   ```bash
   git clone https://github.com/Macmillan1411/restaurant-booking-api.git
   ```

2. Create a `.env` file in the project root with the following content:
   ```
   # Database
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=postgres
   POSTGRES_DB=restaurant
   
   # API
   DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/restaurant
   ```

3. Build and start the services:
   ```bash
   docker-compose up -d
   ```

4. The API will be available at http://localhost:8000

5. Access the interactive API documentation at http://localhost:8000/docs

## API Endpoints

### Tables
- `GET /tables/` - List all tables
- `POST /tables/` - Create a new table
- `DELETE /tables/{id}` - Remove a table

### Reservations
- `GET /reservations/` - List all reservations
- `POST /reservations/` - Create a new reservation
- `DELETE /reservations/{id}` - Cancel a reservation

