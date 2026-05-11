from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas.orders import OrderItemResponse
from database.postgres.repositories.order import OrderRepository
from database.postgres.repositories.order_item import OrderItemRepository
from database.postgres.repositories.product import ProductRepository


class OrderItemService:
    @classmethod
    async def get_by_order_id(
        cls,
        session: AsyncSession,
        order_id: UUID,
        user_id: UUID,
    ) -> list[OrderItemResponse] | None:
        order = await OrderRepository.get_by_id(session=session, order_id=order_id)
        if order is None or order.user_id != user_id:
            return None

        items = await OrderItemRepository.get_by_order_id(session=session, order_id=order_id)
        return [OrderItemResponse.model_validate(item) for item in items]

    @classmethod
    async def get_by_id(
        cls,
        session: AsyncSession,
        order_id: UUID,
        order_item_id: UUID,
        user_id: UUID,
    ) -> OrderItemResponse | None:
        order = await OrderRepository.get_by_id(session=session, order_id=order_id)
        if order is None or order.user_id != user_id:
            return None

        order_item = await OrderItemRepository.get_by_id(session=session, order_item_id=order_item_id)
        if order_item is None or order_item.order_id != order_id:
            return None

        return OrderItemResponse.model_validate(order_item)

    @classmethod
    async def create(
        cls,
        session: AsyncSession,
        order_id: UUID,
        product_id: UUID,
        quantity: int,
        user_id: UUID,
    ) -> OrderItemResponse | None:
        order = await OrderRepository.get_by_id(session=session, order_id=order_id)
        if order is None or order.user_id != user_id:
            return None

        product = await ProductRepository.get_by_id(session=session, product_id=product_id)
        if product is None:
            return None

        price = product.base_price
        total_price = price * quantity

        order_item = await OrderItemRepository.create(
            session=session,
            order_id=order_id,
            product_id=product_id,
            quantity=quantity,
            price=price,
            total_price=total_price,
        )

        order.total_amount = sum(item.total_price for item in order.items) + total_price
        return OrderItemResponse.model_validate(order_item)
