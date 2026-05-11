from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from database.postgres.models.unit import ProductUnit


class PhotoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    file_name: str
    mime_type: str
    file_size: int
    created_at: datetime
    updated_at: datetime


class CreateProductRequest(BaseModel):
    name: str
    description: str | None = None
    base_price: Decimal
    unit: ProductUnit
    is_active: bool = True


class ProductShortResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    base_price: Decimal
    unit: ProductUnit


class ProductResponse(ProductShortResponse):
    description: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    photos: list[PhotoResponse] = []
