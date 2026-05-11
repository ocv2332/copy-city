from .orders import router as orders_router
from .photos import router as photos_router
from .products import router as products_router

__all__ = ["orders_router", "photos_router", "products_router"]
