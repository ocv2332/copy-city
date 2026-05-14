# Copy City Frontend

React-фронтенд для сервисов `auth` и `backend`.

## Запуск

```bash
cd frontend
npm install
npm run dev
```

По умолчанию приложение ходит в:

- `http://localhost:8000/api/v1` для авторизации
- `http://localhost:8001/api/v1` для товаров, фото и заказов

Если адреса отличаются, создайте `.env` рядом с `.env.example` и переопределите:

```env
VITE_AUTH_API_URL=http://localhost:8000/api/v1
VITE_BACKEND_API_URL=http://localhost:8001/api/v1
```
