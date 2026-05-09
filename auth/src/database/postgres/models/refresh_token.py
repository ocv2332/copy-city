import uuid
from datetime import datetime
from uuid import UUID

from sqlalchemy import Uuid, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.postgres.models import Base
from database.postgres.constants import REFRESH_TOKEN_MAX_LENGTH, MOSCOW_TZ


class RefreshToken(Base):
    __tablename__ = "refresh_token"

    id: Mapped[UUID] = mapped_column(Uuid(), primary_key=True, default=uuid.uuid4)
    token: Mapped[str] = mapped_column(String(REFRESH_TOKEN_MAX_LENGTH), unique=True, nullable=False)
    expiration_date: Mapped[datetime] = mapped_column(DateTime(timezone=MOSCOW_TZ), nullable=False)

    session: Mapped["Session"] = relationship("Session", back_populates="refresh_token")
