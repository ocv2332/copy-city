from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from api.deps import require_admin
from api.schemas.products import CreateProductRequest, ProductResponse
from core.services.products import ProductService
from database.postgres.sessions.uow import unit_of_work

router = APIRouter()
product_service = ProductService()


@router.get(
    "",
    response_model=list[ProductResponse],
    summary="Получить список продуктов",
    description="Возвращает список всех продуктов. Метод доступен без авторизации.",
)
async def get_products():
    async with unit_of_work() as uow:
        return await product_service.get_all_products(session=uow.session)


@router.get(
    "/{product_id}",
    response_model=ProductResponse,
    summary="Получить продукт по идентификатору",
    description="Возвращает полную информацию о продукте и его фотографиях. Метод доступен без авторизации.",
)
async def get_product_by_id(product_id: UUID):
    async with unit_of_work() as uow:
        product = await product_service.get_by_id(session=uow.session, product_id=product_id)
        if product is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Продукт не найден")
        return product


@router.post(
    "",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_admin)],
    summary="Создать продукт",
    description="Создает новый продукт. Метод доступен только администратору.",
)
async def create_product(body: CreateProductRequest):
    async with unit_of_work() as uow:
        return await product_service.create(
            session=uow.session,
            name=body.name,
            description=body.description,
            base_price=body.base_price,
            unit=body.unit,
            is_active=body.is_active,
        )
