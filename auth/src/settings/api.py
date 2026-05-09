from settings.base import Settings


class ApiSettings(Settings):
    TITLE: str = "auth"
    OPENAPI_URL: str | None = "/api/openapi.json"
    DOCS_URL: str | None = "/api/docs"
    REDOC_URL: str | None = None
    ORIGINS: list[str] = ["*"]


settings = ApiSettings()