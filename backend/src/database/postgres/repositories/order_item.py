from typing import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from database.postgres.models import OrderItem


class OrderItemRepository:
    @classmethod
    async def get_by_id(cls, session: AsyncSession, order_item_id: UUID) -> OrderItem | None:
        query = select(OrderItem).options(selectinload(OrderItem.product)).where(OrderItem.id == order_item_id)
        return (await session.execute(query)).scalar_one_or_none()

    @classmethod
    async def get_by_order_id(cls, session: AsyncSession, order_id: UUID) -> Sequence[OrderItem]:
        query = select(
            OrderItem
        ).options(
            selectinload(OrderItem.order),
            selectinload(OrderItem.product)
        ).where(OrderItem.order_id == order_id)

        return (await session.execute(query)).scalars().all()

    @classmethod
    async def create(cls, session: AsyncSession, order_id: UUID, product_id: UUID, quantity: int, price: float, total_price: float) -> OrderItem:
        order_item = OrderItem(
            order_id=order_id,
            product_id=product_id,
            quantity=quantity,
            price=price,
            total_price=total_price,
        )
        session.add(order_item)
        await session.flush()
        await session.refresh(order_item, attribute_names=["product"])

        return order_item
