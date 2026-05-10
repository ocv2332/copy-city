from fastapi import Depends, HTTPException, status

from api.deps.auth import get_token_payload
from database.postgres.models.user_roles import UserRoles


async def require_admin(payload: dict = Depends(get_token_payload)) -> dict:
    print(payload.get("role"))
    if payload.get("role") != UserRoles.admin.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return payload
