from uuid import UUID

from api.schemas.orders import OrderResponse
from database.postgres.repositories.order import OrderRepository
from database.postgres.models.unit import OrderStatus
from sqlalchemy.ext.asyncio import AsyncSession


class OrderService:
    @classmethod
    async def get_by_user_id(cls, session: AsyncSession, user_id: UUID) -> list[OrderResponse]:
        orders = await OrderRepository.get_by_user_id(session=session, user_id=user_id)
        return [OrderResponse.model_validate(order) for order in orders]

    @classmethod
    async def get_by_id(cls, session: AsyncSession, order_id: UUID, user_id: UUID) -> OrderResponse | None:
        order = await OrderRepository.get_by_id(session=session, order_id=order_id)
        if order is None or order.user_id != user_id:
            return None
        return OrderResponse.model_validate(order)

    @classmethod
    async def create(cls, session: AsyncSession, user_id: UUID, total_amount, comment: str | None) -> OrderResponse:
        order = await OrderRepository.create(
            session=session,
            user_id=user_id,
            total_amount=total_amount,
            comment=comment,
        )
        return OrderResponse.model_validate(order)

    @classmethod
    async def update_status(
        cls,
        session: AsyncSession,
        order_id: UUID,
        user_id: UUID,
        status: OrderStatus,
    ) -> OrderResponse | None:
        order = await OrderRepository.get_by_id(session=session, order_id=order_id)
        if order is None or order.user_id != user_id:
            return None

        updated_order = await OrderRepository.update(
            session=session,
            order_id=order_id,
            status=status,
        )
        if updated_order is None:
            return None
        return OrderResponse.model_validate(updated_order)
