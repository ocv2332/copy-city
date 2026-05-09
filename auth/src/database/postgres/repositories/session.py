from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from database.postgres.models import Session


class SessionRepository:
    @classmethod
    async def create(
        cls,
        session: AsyncSession,
        user_id: UUID,
        refresh_token_id: UUID,
        user_agent: str,
    ) -> Session:
        user_session = Session(
            user_id=user_id,
            refresh_token_id=refresh_token_id,
            user_agent=user_agent,
        )
        session.add(user_session)
        await session.flush()
        return user_session

    @classmethod
    async def get_by_refresh_token_id(
        cls,
        session: AsyncSession,
        refresh_token_id: UUID,
    ) -> Session | None:
        query = (
            select(Session)
            .options(selectinload(Session.user))
            .where(Session.refresh_token_id == refresh_token_id)
        )
        return (await session.execute(query)).scalar_one_or_none()
