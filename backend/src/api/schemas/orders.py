from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from api.schemas.products import ProductShortResponse
from database.postgres.models.unit import OrderStatus


class CreateOrderRequest(BaseModel):
    total_amount: Decimal
    comment: str | None = None


class CreateOrderItemRequest(BaseModel):
    product_id: UUID
    quantity: int


class OrderItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    product_id: UUID
    quantity: int
    price: Decimal
    total_price: Decimal
    product: ProductShortResponse | None = None


class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    status: OrderStatus
    total_amount: Decimal
    comment: str | None
    created_at: datetime
    updated_at: datetime
    items: list[OrderItemResponse] = []
