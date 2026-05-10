from datetime import datetime, timedelta
from uuid import UUID

from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute

from api.schemas import (
    RequestUsers,
    ResponseUsers,
    TokenResponse,
)
from core.services.security import (
    build_access_token_redis_key,
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
)
from database.postgres.constants import MOSCOW_TZ
from database.postgres.models import Users
from database.postgres.models.user_roles import UserRoles
from database.postgres.repositories import (
    AuthSessionRepository,
    RefreshTokenRepository,
    SessionRepository,
    UsersRepository,
)
from settings.jwt import settings as jwt_settings

user_repository = UsersRepository()
refresh_token_repository = RefreshTokenRepository()
session_repository = SessionRepository()
auth_session_repository = AuthSessionRepository()


class UserService:
    @classmethod
    async def get_user_by_id(cls, session: AsyncSession, user_id) -> Users | None:
        return await user_repository.get(session=session, user_id=user_id)

    @classmethod
    async def get_user_by_email(cls, session: AsyncSession, email: str) -> Users | None:
        return await user_repository.get_user_by_email(session=session, email=email)

    @classmethod
    async def authenticate_user(
            cls,
            session: AsyncSession,
            email: str,
            password: str,
    ) -> Users | None:
        user: Users = await cls.get_user_by_email(session=session, email=email)
        if user is None:
            return None

        hashed_password: str = str(user.hashed_password)
        if not verify_password(password, hashed_password):
            return None

        return user

    @classmethod
    async def create_user(cls, session: AsyncSession, body: RequestUsers) -> ResponseUsers | None:
        hashed_password = hash_password(body.password.get_secret_value())

        user = await user_repository.create(
            session=session,
            email=body.email,
            lastname=body.lastname,
            firstname=body.firstname,
            date_of_birth=body.date_of_birth,
            hashed_password=hashed_password,
            middle_name=body.middle_name,
        )
        return ResponseUsers.model_validate(user)

    @classmethod
    async def login(
        cls,
        session: AsyncSession,
        redis: Redis | None,
        email: str,
        password: str,
        user_agent: str,
    ) -> tuple[TokenResponse, InstrumentedAttribute[str]] | None:
        user: Users = await cls.authenticate_user(
            session=session,
            email=email,
            password=password,
        )
        if user is None:
            return None

        refresh_token_value = create_refresh_token()
        expiration_date = datetime.now(tz=MOSCOW_TZ) + timedelta(
            seconds=jwt_settings.REFRESH_TOKEN_LIFETIME_SECONDS
        )
        refresh_token = await refresh_token_repository.create(
            session=session,
            token=refresh_token_value,
            expiration_date=expiration_date,
        )
        user_id: UUID = user.id  # type: ignore[arg-type]
        await session_repository.create(
            session=session,
            user_id=user_id,
            refresh_token_id=refresh_token.id,  # type: ignore[arg-type]
            user_agent=user_agent,
        )
        access_token, jti, ttl = create_access_token(user_id, user.role.value)
        if redis is not None:
            await redis.set(build_access_token_redis_key(jti), str(user.id), ex=ttl)
        return TokenResponse(
            access_token=access_token,
        ), refresh_token.token

    @classmethod
    async def refresh_tokens(
        cls,
        session: AsyncSession,
        redis: Redis | None,
        refresh_token_value: str,
    ) -> tuple[TokenResponse, str] | None:
        refresh_token = await refresh_token_repository.get_by_token(
            session=session,
            token=refresh_token_value,
        )
        if refresh_token is None:
            return None
        if refresh_token.expiration_date < datetime.now(tz=MOSCOW_TZ):
            return None
        refresh_token_id: UUID = refresh_token.id  # type: ignore[arg-type]
        user_session = await session_repository.get_by_refresh_token_id(
            session=session,
            refresh_token_id=refresh_token_id,
        )
        if user_session is None:
            return None

        refresh_token.token = create_refresh_token()
        refresh_token.expiration_date = datetime.now(tz=MOSCOW_TZ) + timedelta(
            seconds=jwt_settings.REFRESH_TOKEN_LIFETIME_SECONDS
        )
        await session.flush()
        access_token, jti, ttl = create_access_token(user_session.user.id, user_session.user.role.value)
        if redis is not None:
            await redis.set(build_access_token_redis_key(jti), str(user_session.user.id), ex=ttl)

        refresh_token_value: str = str(refresh_token.token)

        return TokenResponse(
            access_token=access_token,
        ), refresh_token_value

    @classmethod
    async def logout(
        cls,
        session: AsyncSession,
        redis: Redis | None,
        refresh_token_value: str | None,
        access_token_jti: str | None,
    ) -> None:
        if access_token_jti is not None and redis is not None:
            await redis.delete(build_access_token_redis_key(access_token_jti))

        if refresh_token_value is None:
            return

        refresh_token = await refresh_token_repository.get_by_token(
            session=session,
            token=refresh_token_value,
        )
        if refresh_token is None:
            return

        await auth_session_repository.delete_by_refresh_token_id(
            session=session,
            refresh_token_id=refresh_token.id,
        )
        await refresh_token_repository.delete(session=session, refresh_token=refresh_token)

    @classmethod
    async def update_user_roles(cls, session: AsyncSession, user_id: UUID, role: UserRoles) -> ResponseUsers | None:
        return await user_repository.update_user_roles(session=session, user_id=user_id, role=role)
