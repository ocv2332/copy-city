from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas.products import PhotoResponse
from database.postgres.repositories.photo import PhotoRepository
from database.postgres.repositories.product import ProductRepository


class PhotoService:
    @classmethod
    async def get_by_id(cls, session: AsyncSession, photo_id: UUID):
        return await PhotoRepository.get_by_id(session=session, photo_id=photo_id)

    @classmethod
    async def get_by_product_id(cls, session: AsyncSession, product_id: UUID) -> list[PhotoResponse]:
        photos = await PhotoRepository.get_all_by_product_id(session=session, product_id=product_id)
        return [PhotoResponse.model_validate(photo) for photo in photos]

    @classmethod
    async def create(
        cls,
        session: AsyncSession,
        product_id: UUID,
        file_name: str,
        mime_type: str,
        file_size: int,
        file_data: bytes,
    ) -> PhotoResponse | None:
        product = await ProductRepository.get_by_id(session=session, product_id=product_id)
        if product is None:
            return None

        photo = await PhotoRepository.create(
            session=session,
            product_id=product_id,
            file_name=file_name,
            mime_type=mime_type,
            file_size=file_size,
            file_data=file_data,
        )
        return PhotoResponse.model_validate(photo)
