from fastapi import HTTPException, status

from api.deps.auth import UserData


async def require_admin(userData: UserData) -> None:
    if userData.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Доступ разрешен только администратору",
        )
