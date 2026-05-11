from datetime import datetime
from typing import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from database.constants import MOSCOW_TZ
from database.postgres.models import Product
from database.postgres.models.unit import ProductUnit


class ProductRepository:
    @classmethod
    async def get_by_id(cls, session: AsyncSession, product_id: UUID) -> Product | None:
        query = select(Product).options(selectinload(Product.photos)).where(Product.id == product_id)
        return (await session.execute(query)).scalar_one_or_none()

    @classmethod
    async def get_by_name(cls, session: AsyncSession, name: str) -> Product | None:
        query = select(Product).where(Product.name == name)
        return (await session.execute(query)).scalar_one_or_none()

    @classmethod
    async def get_all_products(cls, session: AsyncSession) -> Sequence[Product]:
        query = select(Product).options(selectinload(Product.photos))

        return (await session.execute(query)).scalars().all()

    @classmethod
    async def create(
        cls,
        session: AsyncSession,
        name: str,
        description: str | None,
        base_price,
        unit: ProductUnit,
        is_active: bool,
    ) -> Product:
        date_now = datetime.now(tz=MOSCOW_TZ)
        product = Product(
            name=name,
            description=description,
            base_price=base_price,
            unit=unit,
            is_active=is_active,
            created_at=date_now,
            updated_at=date_now,
        )
        session.add(product)
        await session.flush()
        await session.refresh(product, attribute_names=["photos"])
        return product
