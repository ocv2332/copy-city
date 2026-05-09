from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.postgres.models import RefreshToken


class RefreshTokenRepository:
    @classmethod
    async def get_by_token(cls, session: AsyncSession, token: str) -> RefreshToken | None:
        query = select(RefreshToken).where(RefreshToken.token == token)
        return (await session.execute(query)).scalar_one_or_none()

    @classmethod
    async def create(
        cls,
        session: AsyncSession,
        token: str,
        expiration_date: datetime,
    ) -> RefreshToken:
        refresh_token = RefreshToken(token=token, expiration_date=expiration_date)
        session.add(refresh_token)
        await session.flush()
        return refresh_token

    @classmethod
    async def delete(cls, session: AsyncSession, refresh_token: RefreshToken) -> None:
        await session.delete(refresh_token)
