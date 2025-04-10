# Система Бронирования Ресторана

Современный REST API сервис для управления бронированием столиков в ресторане, построенный на FastAPI и PostgreSQL.

## Возможности

- ✨ Управление столиками ресторана (создание, просмотр, удаление)
- 🕒 Система бронирования с обнаружением конфликтов по времени
- 📝 Полная документация API
- 🔒 Валидация данных
- 🐳 Docker-контейнеризация
- 🧪 Полное тестовое покрытие

## Технологический стек

- FastAPI
- PostgreSQL
- SQLModel
- Pydantic
- Docker
- Poetry
- Alembic (миграции)
- Pytest (тестирование)

## Быстрый старт

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/Macmillan1411/restaurant-booking-api.git
   ```

2. Создайте файл `.env` в корне проекта:
   ```env
   # База данных
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=postgres
   POSTGRES_DB=restaurant
   ```

3. Запустите сервисы:
   ```bash
   docker-compose up -d
   ```

4. API будет доступен по адресу: http://localhost:8000
5. Интерактивная документация: http://localhost:8000/docs

## API Endpoints

### Столики
- `GET /tables/` - Список всех столиков
- `POST /tables/` - Создать новый столик
- `DELETE /tables/{id}` - Удалить столик

### Бронирования
- `GET /reservations/` - Список всех бронирований
- `POST /reservations/` - Создать новое бронирование
- `DELETE /reservations/{id}` - Отменить бронирование

## Разработка

### Установка зависимостей
```bash
poetry install
```

### Запуск тестов
```bash
poetry run pytest
```

### Применение миграций
```bash
poetry run alembic upgrade head
```

## Архитектура

Проект следует принципам чистой архитектуры:
- 📝 Schemas - валидация данных и API контракты
- 🎯 Services - бизнес-логика
- 🗄️ Models - модели данных
- 🛣️ Routers - маршрутизация API
- 🔧 Core - основные конфигурации и утилиты

## Тестирование

- ✅ Модульные тесты
- ✅ Интеграционные тесты
- ✅ Асинхронное тестирование
- ✅ Фикстуры для тестовой базы данных

## Автор

Macmillan1411 (macmillantapiwanashe1411@gmail.com)

