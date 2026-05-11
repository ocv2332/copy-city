from datetime import datetime
from typing import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.constants import MOSCOW_TZ
from database.postgres.models import Photo


class PhotoRepository:
    @classmethod
    async def get_by_id(cls, session: AsyncSession, photo_id: UUID) -> Photo | None:
        return await session.get(Photo, photo_id)

    @classmethod
    async def get_by_product_id(cls, session: AsyncSession, product_id: UUID) -> Photo | None:
        query = select(Photo).where(Photo.product_id == product_id)
        return (await session.execute(query)).scalar_one_or_none()

    @classmethod
    async def get_all_by_product_id(cls, session: AsyncSession, product_id: UUID) -> Sequence[Photo]:
        query = select(Photo).where(Photo.product_id == product_id)
        return (await session.execute(query)).scalars().all()

    @classmethod
    async def create(cls, session: AsyncSession, product_id: UUID, file_name: str, mime_type: str, file_size: int, file_data: bytes) -> Photo:
        date_now = datetime.now(tz=MOSCOW_TZ)

        photo = Photo(
            product_id=product_id,
            file_name=file_name,
            mime_type=mime_type,
            file_size=file_size,
            file_data=file_data,
            created_at=date_now,
            updated_at=date_now,
        )

        session.add(photo)
        await session.flush()
        return photo

    @classmethod
    async def update(cls, session: AsyncSession, photo_id: UUID, file_name: str, mime_type: str, file_size: int, file_data: bytes) -> Photo | None:
        date_now = datetime.now(tz=MOSCOW_TZ)

        photo = await cls.get_by_id(session, photo_id)
        if photo is None:
            return None

        photo.file_name = file_name
        photo.mime_type = mime_type
        photo.file_size = file_size
        photo.file_data = file_data
        photo.updated_at = date_now

        session.add(photo)
        await session.flush()

        return photo

    @classmethod
    async def delete(cls, session: AsyncSession, photo_id: UUID) -> str | None:
        photo = await cls.get_by_id(session, photo_id)
        if photo is None:
            return None

        await session.delete(photo)

        return "deleted"
