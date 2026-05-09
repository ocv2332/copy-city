from pydantic import field_validator
from pydantic_core.core_schema import FieldValidationInfo

from settings.base import Settings


class DatabaseSettings(Settings):
    ASYNC_POSTGRES_DATABASE_URL: str
    SYNC_POSTGRES_DATABASE_URL: str
    POSTGRES_AUTH_DB: str
    LOG_QUERIES: bool = False
    ASYNC_DATABASE_URL: str = None
    SYNC_DATABASE_URL: str = None

    REDIS_URL: str

    @classmethod
    def _assemble_dsn(cls, database_url: str, db: str):
        return f"{database_url}{db}"

    @field_validator("ASYNC_DATABASE_URL", mode="before")
    @classmethod
    def validate_async_dsn(cls, v: str | None, info: FieldValidationInfo):
        database_url = info.data["ASYNC_POSTGRES_DATABASE_URL"]
        db = info.data["POSTGRES_AUTH_DB"]
        return cls._assemble_dsn(database_url, db)

    @field_validator("SYNC_DATABASE_URL", mode="before")
    @classmethod
    def validate_sync_dsn(cls, v: str | None, info: FieldValidationInfo):
        database_url = info.data["SYNC_POSTGRES_DATABASE_URL"]
        db = info.data["POSTGRES_AUTH_DB"]
        return cls._assemble_dsn(database_url, db)


settings = DatabaseSettings()
