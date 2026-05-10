import uuid
from datetime import datetime

from sqlalchemy import Uuid, ForeignKey, String, Integer, LargeBinary, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.constants import NAME_PHOTO_MAX_LENGTH, MIME_TYPE_MAX_LENGTH, MOSCOW_TZ
from database.postgres.models.base import Base


class Photo(Base):
    __tablename__ = "photos"
    __table_args__ = {"schema": "backend"}

    id: Mapped[uuid.UUID] = mapped_column(Uuid(), primary_key=True, default=uuid.uuid4)

    product_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("backend.products.id"), nullable=False)
    file_name: Mapped[str] = mapped_column(String(NAME_PHOTO_MAX_LENGTH), nullable=False)
    mime_type: Mapped[str] = mapped_column(String(MIME_TYPE_MAX_LENGTH), nullable=False)
    file_size: Mapped[int] = mapped_column(Integer, nullable=False)
    file_data: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=MOSCOW_TZ), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=MOSCOW_TZ), nullable=False)

    product: Mapped["Product"] = relationship("Product", back_populates="photos")