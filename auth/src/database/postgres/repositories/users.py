from datetime import date, datetime
from uuid import UUID

from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.postgres.models import Users
from database.postgres.constants import MOSCOW_TZ
from database.postgres.models.user_roles import UserRoles


class UsersRepository:
    @classmethod
    async def get(cls, session: AsyncSession, user_id: UUID) -> Users | None:
        return await session.get(Users, user_id)

    @classmethod
    async def get_user_by_email(cls, session: AsyncSession, email: str) -> Users | None:
        query = select(Users).where(Users.email == email)
        return (await session.execute(query)).scalar_one_or_none()

    @classmethod
    async def create(
            cls,
            session: AsyncSession,
            email: EmailStr,
            lastname: str,
            firstname: str,
            date_of_birth: date,
            hashed_password: str,
            middle_name: str | None = None,
    ) -> Users | None:
        user = Users(
            email=email,
            lastname=lastname,
            firstname=firstname,
            middle_name=middle_name,
            date_of_birth=date_of_birth,
            hashed_password=hashed_password,
            role=UserRoles.user,
            created_at=datetime.now(tz=MOSCOW_TZ),
            updated_at=datetime.now(tz=MOSCOW_TZ),
        )
        session.add(user)
        await session.flush()

        return user

    @classmethod
    async def update_user_roles(cls, session: AsyncSession, user_id: UUID, role: UserRoles) -> Users | None:
        user = await session.get(Users, user_id)

        if user is None:
            return None

        user.roles = role
        await session.flush()
        return user
