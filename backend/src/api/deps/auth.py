import json
from typing import Annotated
from urllib import error, request

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from api.schemas.auth import AuthorizedUser
from settings.auth import settings as auth_settings

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{auth_settings.AUTH_SERVICE_URL.rstrip('/')}{auth_settings.AUTH_LOGIN_PATH}"
)


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
) -> AuthorizedUser:
    auth_request = request.Request(
        url=f"{auth_settings.AUTH_SERVICE_URL.rstrip('/')}{auth_settings.AUTH_CHECK_PATH}",
        headers={
            "Authorization": f"Bearer {token}",
        },
        method="GET",
    )

    try:
        with request.urlopen(auth_request, timeout=auth_settings.AUTH_REQUEST_TIMEOUT) as response:
            payload = json.loads(response.read().decode())
            return AuthorizedUser.model_validate(payload)
    except error.HTTPError as exc:
        if exc.code == status.HTTP_401_UNAUTHORIZED:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Недействительный или истекший токен доступа",
            ) from exc
        if exc.code == status.HTTP_404_NOT_FOUND:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Пользователь не найден",
            ) from exc
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Сервис авторизации вернул неожиданный ответ",
        ) from exc
    except error.URLError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Сервис авторизации недоступен",
        ) from exc


UserData = Annotated[AuthorizedUser, Depends(get_current_user)]
