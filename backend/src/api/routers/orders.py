from uuid import UUID

from fastapi import APIRouter, HTTPException, status, Depends

from api.deps import UserData, require_admin
from api.schemas.orders import CreateOrderItemRequest, CreateOrderRequest, OrderItemResponse, OrderResponse
from core.services.order_items import OrderItemService
from core.services.orders import OrderService
from database.postgres.models.unit import OrderStatus
from database.postgres.sessions.uow import unit_of_work

router = APIRouter()
order_service = OrderService()
order_item_service = OrderItemService()


@router.get(
    "",
    response_model=list[OrderResponse],
    summary="Получить список заказов текущего пользователя",
    description="Возвращает все заказы авторизованного пользователя вместе с позициями заказа.",
)
async def get_my_orders(userData: UserData):
    async with unit_of_work() as uow:
        return await order_service.get_by_user_id(session=uow.session, user_id=userData.id)


@router.get(
    "/{order_id}",
    response_model=OrderResponse,
    summary="Получить заказ по идентификатору",
    description="Возвращает один заказ текущего пользователя по его идентификатору.",
)
async def get_order_by_id(order_id: UUID, userData: UserData):
    async with unit_of_work() as uow:
        order = await order_service.get_by_id(session=uow.session, order_id=order_id, user_id=userData.id)
        if order is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Заказ не найден")
        return order


@router.post(
    "",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создать заказ",
    description="Создает новый заказ для текущего пользователя. Сразу после создания заказ может быть пустым, позиции добавляются отдельно.",
)
async def create_order(body: CreateOrderRequest, userData: UserData):
    async with unit_of_work() as uow:
        return await order_service.create(
            session=uow.session,
            user_id=userData.id,
            total_amount=body.total_amount,
            comment=body.comment,
        )


@router.patch(
    "/{order_id}/status",
    response_model=OrderResponse,
    summary="Изменить статус заказа",
    description="Изменяет статус существующего заказа текущего пользователя.",
    dependencies=[Depends(require_admin)],
)
async def update_order_status(order_id: UUID, status_value: OrderStatus):
    async with unit_of_work() as uow:
        order = await order_service.update_status(
            session=uow.session,
            order_id=order_id,
            status=status_value,
        )
        if order is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Заказ не найден")
        return order


@router.get(
    "/{order_id}/items",
    response_model=list[OrderItemResponse],
    summary="Получить позиции заказа",
    description="Возвращает список всех позиций выбранного заказа текущего пользователя.",
)
async def get_order_items(order_id: UUID, userData: UserData):
    async with unit_of_work() as uow:
        items = await order_item_service.get_by_order_id(
            session=uow.session,
            order_id=order_id,
            user_id=userData.id,
        )
        if items is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Заказ не найден")
        return items


@router.get(
    "/{order_id}/items/{order_item_id}",
    response_model=OrderItemResponse,
    summary="Получить позицию заказа",
    description="Возвращает одну позицию выбранного заказа текущего пользователя.",
)
async def get_order_item(order_id: UUID, order_item_id: UUID, userData: UserData):
    async with unit_of_work() as uow:
        item = await order_item_service.get_by_id(
            session=uow.session,
            order_id=order_id,
            order_item_id=order_item_id,
            user_id=userData.id,
        )
        if item is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Позиция заказа не найдена")
        return item


@router.post(
    "/{order_id}/items",
    response_model=OrderItemResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Добавить позицию в заказ",
    description="Добавляет новый продукт в выбранный заказ текущего пользователя. Цена позиции рассчитывается на backend.",
)
async def create_order_item(order_id: UUID, body: CreateOrderItemRequest, userData: UserData):
    async with unit_of_work() as uow:
        item = await order_item_service.create(
            session=uow.session,
            order_id=order_id,
            product_id=body.product_id,
            quantity=body.quantity,
            user_id=userData.id,
        )
        if item is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Заказ или продукт не найден",
            )
        return item
