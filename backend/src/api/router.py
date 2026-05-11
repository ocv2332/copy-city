from fastapi import APIRouter

from api.routers import orders_router, photos_router, products_router

router = APIRouter(prefix="/api")
router.include_router(products_router, prefix="/v1/products", tags=["Продукты"])
router.include_router(orders_router, prefix="/v1/orders", tags=["Заказы"])
router.include_router(photos_router, prefix="/v1", tags=["Фотографии"])
