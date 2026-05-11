from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from api.router import router
from database.postgres.sessions import session as postgresql
from settings.api import settings as api_settings
from settings.database import settings as database_settings


@asynccontextmanager
async def lifespan(_: FastAPI):
    postgresql.async_engine = create_async_engine(
        database_settings.ASYNC_DATABASE_URL,
        echo=database_settings.LOG_QUERIES,
        connect_args={
            "server_settings": {
                "search_path": "backend,public",
            }
        },
    )
    postgresql.async_session = async_sessionmaker(postgresql.async_engine, expire_on_commit=False)
    yield
    await postgresql.async_engine.dispose()


app = FastAPI(
    title=api_settings.TITLE,
    openapi_url=api_settings.OPENAPI_URL,
    docs_url=api_settings.DOCS_URL,
    redoc_url=api_settings.REDOC_URL,
    lifespan=lifespan,
    root_path="/backend",
)

app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=api_settings.ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
