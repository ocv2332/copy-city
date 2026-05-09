from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from core.services.security import build_access_token_redis_key, decode_access_token
from database.postgres.sessions.redis import get_redis

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/api/v1/login")


async def get_token_payload(
    token: Annotated[str, Depends(oauth2_scheme)],
):
    try:
        payload = decode_access_token(token)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        ) from exc

    redis = await get_redis()
    if redis is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Redis is unavailable",
        )

    jti = payload.get("jti")
    if not isinstance(jti, str):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )

    token_exists = await redis.exists(build_access_token_redis_key(jti))
    if not token_exists:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token is revoked or expired",
        )
    return payload


async def get_current_user_id(payload: Annotated[dict, Depends(get_token_payload)]) -> UUID:
    try:
        return UUID(payload["sub"])
    except (KeyError, ValueError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token subject",
        ) from exc
