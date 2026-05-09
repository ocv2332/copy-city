from datetime import date, datetime
import uuid

from pydantic import EmailStr
from sqlalchemy import Uuid, String, Date, Enum as AlchEnum, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID

from database.postgres.models import Base
from database.postgres.constants import EMAIL_LENGTH_MAX_LENGTH, NAME_STR_LEN, MOSCOW_TZ, \
    HASHED_PASSWORD_MAX_LENGTH
from database.postgres.models.user_roles import UserRoles


class Users(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(Uuid(), primary_key=True, default=uuid.uuid4)

    email: Mapped[EmailStr] = mapped_column(String(length=EMAIL_LENGTH_MAX_LENGTH), unique=True, index=True, nullable=False)
    lastname: Mapped[String] = mapped_column(String(length=NAME_STR_LEN), nullable=False)
    firstname: Mapped[String] = mapped_column(String(length=NAME_STR_LEN), nullable=False)
    middle_name: Mapped[String] = mapped_column(String(length=NAME_STR_LEN), nullable=True)
    date_of_birth: Mapped[date] = mapped_column(Date, nullable=False)
    role: Mapped[UserRoles] = mapped_column(AlchEnum(UserRoles, name="user_roles", schema="auth", create_type=True), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(length=HASHED_PASSWORD_MAX_LENGTH), nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=MOSCOW_TZ), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=MOSCOW_TZ), nullable=False)

    sessions: Mapped[list["Session"]] = relationship("Session", back_populates="user")
