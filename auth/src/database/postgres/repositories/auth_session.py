from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from database.postgres.models import Session


class AuthSessionRepository:
    @classmethod
    async def delete_by_refresh_token_id(cls, session: AsyncSession, refresh_token_id) -> None:
        await session.execute(
            delete(Session).where(Session.refresh_token_id == refresh_token_id)
        )
