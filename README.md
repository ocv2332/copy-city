# Copy City

Web-приложение для сайта "Копир Город".

Проект состоит из трех частей:

- `auth` - сервис авторизации на FastAPI.
- `backend` - основной API на FastAPI.
- `frontend` - React/Vite приложение.

Инфраструктура запускается через Docker Compose: PostgreSQL и Redis.

## Требования

- Docker и Docker Compose
- Node.js 18+ и npm

## Настройка окружения

Создайте корневой файл `.env` из примера:

```bash
cp example.env .env
```

Заполните переменные:

```env
POSTGRES_DB=copy_city
POSTGRES_USER=copy_city
POSTGRES_PASSWORD=copy_city_password
POSTGRES_PORT=5432

REDIS_PASSWORD=redis_password
REDIS_PORT=6379

ASYNC_POSTGRES_DATABASE_URL=postgresql+asyncpg://copy_city:copy_city_password@postgres:5432/
SYNC_POSTGRES_DATABASE_URL=postgresql+psycopg://copy_city:copy_city_password@postgres:5432/
POSTGRES_AUTH_DB=copy_city

REDIS_URL=redis://:redis_password@redis:6379/0
LOG_QUERIES=false
SECRET_KEY=change-me
```

Для локального запуска frontend создайте `frontend/.env`:

```bash
cp frontend/example.env frontend/.env
```

И укажите адреса API:

```env
VITE_AUTH_API_URL=http://localhost:8000/api/v1
VITE_BACKEND_API_URL=http://localhost:8001/api/v1
```

## Запуск через Docker

Сначала поднимите PostgreSQL и Redis из корня проекта:

```bash
docker compose -f docker-compose.infra.yml up -d
```

Затем запустите сервис авторизации:

```bash
docker compose -f auth/docker-compose.auth.yml up --build
```

В отдельном терминале запустите основной backend:

```bash
docker compose -f backend/docker-compose.backend.yml up --build
```

При старте `auth` и `backend` автоматически применяют миграции Alembic.

## Запуск frontend

В отдельном терминале:

```bash
cd frontend
npm install
npm run dev
```

Frontend будет доступен по адресу:

```text
http://localhost:5173
```

## Адреса сервисов

- Auth API: `http://localhost:8000/api/v1`
- Auth Swagger: `http://localhost:8000/api/docs`
- Backend API: `http://localhost:8001/api/v1`
- Backend Swagger: `http://localhost:8001/api/docs`
- Frontend: `http://localhost:5173`

## Остановка

Остановить backend:

```bash
docker compose -f backend/docker-compose.backend.yml down
```

Остановить auth:

```bash
docker compose -f auth/docker-compose.auth.yml down
```

Остановить инфраструктуру:

```bash
docker compose -f docker-compose.infra.yml down
```

Чтобы удалить данные PostgreSQL и Redis вместе с контейнерами:

```bash
docker compose -f docker-compose.infra.yml down -v
```

## Полезные команды

Проверить frontend:

```bash
cd frontend
npm run build
```

Посмотреть логи инфраструктуры:

```bash
docker compose -f docker-compose.infra.yml logs -f
```

Посмотреть логи auth:

```bash
docker compose -f auth/docker-compose.auth.yml logs -f
```

Посмотреть логи backend:

```bash
docker compose -f backend/docker-compose.backend.yml logs -f
```
