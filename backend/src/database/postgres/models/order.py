import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import Uuid, ForeignKey, Enum as AlchEnum, Numeric, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.constants import MOSCOW_TZ
from database.postgres.models.base import Base
from database.postgres.models.unit import OrderStatus


class Order(Base):
    __tablename__ = "orders"
    __table_args__ = {"schema": "backend"}

    id: Mapped[uuid.UUID] = mapped_column(Uuid(), primary_key=True, default=uuid.uuid4)

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("auth.users.id"), nullable=False)
    status: Mapped[OrderStatus] = mapped_column(AlchEnum(OrderStatus, name="order_status", schema="backend", create_type=True), nullable=False)
    total_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, default=0)
    comment: Mapped[str | None] = mapped_column(Text(), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=MOSCOW_TZ), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=MOSCOW_TZ), nullable=False)

    items: Mapped[list["OrderItem"]] = relationship("OrderItem", back_populates="order")

    user: Mapped["AuthUser"] = relationship("AuthUser")
