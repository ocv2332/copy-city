from fastapi import APIRouter

from api.routers.auth import router as auth_router

router = APIRouter(prefix="/api")

router.include_router(auth_router, prefix="/v1", tags=["Авторизация"])
