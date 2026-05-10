import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import Uuid, String, Text, Enum as AlchEnum, Boolean, DateTime, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.constants import NAME_PRODUCT_MAX_LENGTH, MOSCOW_TZ
from database.postgres.models.base import Base
from database.postgres.models.unit import ProductUnit


class Product(Base):
    __tablename__ = "products"
    __table_args__ = {"schema": "backend"}

    id: Mapped[uuid.UUID] = mapped_column(Uuid(), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(NAME_PRODUCT_MAX_LENGTH), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text(), nullable=True)
    base_price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    unit: Mapped[ProductUnit] = mapped_column(AlchEnum(ProductUnit, name="product_unit", schema="backend", create_type=True), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=MOSCOW_TZ), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=MOSCOW_TZ), nullable=False)

    photos: Mapped[list["Photo"]] = relationship("Photo", back_populates="product")
    order_items: Mapped[list["OrderItem"]] = relationship("OrderItem", back_populates="product")
