import uuid
from uuid import UUID

from sqlalchemy import Uuid, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.postgres.models import Base, Users, RefreshToken
from database.postgres.constants import USER_AGENT_MAX_LENGTH


class Session(Base):
    __tablename__ = "session"

    id: Mapped[UUID] = mapped_column(Uuid(), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("auth.users.id"), nullable=False)
    refresh_token_id: Mapped[UUID] = mapped_column(ForeignKey("auth.refresh_token.id"), nullable=False)
    user_agent: Mapped[str] = mapped_column(String(USER_AGENT_MAX_LENGTH), nullable=False)

    user: Mapped[Users] = relationship("Users", back_populates="sessions")
    refresh_token: Mapped[RefreshToken] = relationship("RefreshToken", back_populates="session")
