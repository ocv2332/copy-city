from datetime import datetime
from typing import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from database.constants import MOSCOW_TZ
from database.postgres.models import Order
from database.postgres.models.unit import OrderStatus


class OrderRepository:
    @classmethod
    async def get_by_id(cls, session: AsyncSession, order_id: UUID) -> Order | None:
        query = select(Order).options(selectinload(Order.items)).where(Order.id == order_id)
        return (await session.execute(query)).scalar_one_or_none()

    @classmethod
    async def get_by_user_id(cls, session: AsyncSession, user_id: UUID) -> Sequence[Order]:
        query = select(
            Order
        ).options(
            selectinload(Order.items)
        ).where(Order.user_id == user_id)

        return (await session.execute(query)).scalars().all()

    @classmethod
    async def create(cls, session: AsyncSession, user_id: UUID, total_amount: float, comment: str | None) -> Order:
        date_now = datetime.now(tz=MOSCOW_TZ)
        order = Order(
            user_id=user_id,
            status=OrderStatus.new,
            total_amount=total_amount,
            comment=comment,
            created_at=date_now,
            updated_at=date_now,
        )

        session.add(order)
        await session.flush()
        await session.refresh(order, attribute_names=["items"])

        return order

    @classmethod
    async def update(cls, session: AsyncSession, order_id: UUID, status: OrderStatus) -> Order | None:
        order = await cls.get_by_id(session, order_id)

        if order is None:
            return None

        order.status = status
        order.updated_at = datetime.now(tz=MOSCOW_TZ)
        await session.flush()

        return order
