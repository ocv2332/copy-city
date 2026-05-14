from settings.base import Settings


class AuthSettings(Settings):
    AUTH_SERVICE_URL: str = "http://localhost:8000"
    AUTH_SERVICE_URL_DOCKER: str = "http://auth:8000"
    AUTH_LOGIN_PATH: str = "/auth/api/v1/login"
    AUTH_CHECK_PATH: str = "/auth/api/v1/check"
    AUTH_REQUEST_TIMEOUT: float = 5.0


settings = AuthSettings()
