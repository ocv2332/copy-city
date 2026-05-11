from uuid import UUID

from fastapi import HTTPException, status
from api.schemas.products import ProductResponse
from database.postgres.models.unit import ProductUnit
from database.postgres.repositories.product import ProductRepository
from sqlalchemy.ext.asyncio import AsyncSession


class ProductService:
    @classmethod
    async def get_all_products(cls, session: AsyncSession) -> list[ProductResponse]:
        products = await ProductRepository.get_all_products(session=session)
        return [ProductResponse.model_validate(product) for product in products]

    @classmethod
    async def get_by_id(cls, session: AsyncSession, product_id: UUID) -> ProductResponse | None:
        product = await ProductRepository.get_by_id(session=session, product_id=product_id)
        if product is None:
            return None
        return ProductResponse.model_validate(product)

    @classmethod
    async def create(
        cls,
        session: AsyncSession,
        name: str,
        description: str | None,
        base_price,
        unit: ProductUnit,
        is_active: bool,
    ) -> ProductResponse:
        existing_product = await ProductRepository.get_by_name(session=session, name=name)
        if existing_product is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Продукт с таким названием уже существует",
            )

        product = await ProductRepository.create(
            session=session,
            name=name,
            description=description,
            base_price=base_price,
            unit=unit,
            is_active=is_active,
        )
        return ProductResponse.model_validate(product)
