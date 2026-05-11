FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app/backend/src

RUN pip install --no-cache-dir \
    "fastapi>=0.115.0" \
    "uvicorn[standard]>=0.30.0" \
    "sqlalchemy>=2.0.0" \
    "alembic>=1.13.0" \
    "asyncpg>=0.29.0" \
    "psycopg[binary]>=3.2.0" \
    "pydantic[email]>=2.7.0" \
    "pydantic-settings>=2.2.0" \
    "python-multipart>=0.0.9" \
    "greenlet>=3.0.0"

COPY backend/src /app/backend/src

EXPOSE 8001

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
