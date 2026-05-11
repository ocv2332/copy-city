from uuid import UUID

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from fastapi.responses import Response

from api.deps import require_admin
from api.schemas.products import PhotoResponse
from core.services.photos import PhotoService
from database.postgres.sessions.uow import unit_of_work

router = APIRouter()
photo_service = PhotoService()


@router.get(
    "/products/{product_id}/photos",
    response_model=list[PhotoResponse],
    summary="Получить список фотографий продукта",
    description="Возвращает список метаданных фотографий, привязанных к выбранному продукту. Метод доступен без авторизации.",
)
async def get_product_photos(product_id: UUID):
    async with unit_of_work() as uow:
        return await photo_service.get_by_product_id(session=uow.session, product_id=product_id)


@router.get(
    "/photos/{photo_id}",
    summary="Получить фотографию по идентификатору",
    description="Возвращает бинарное содержимое фотографии по ее идентификатору. Метод доступен без авторизации.",
)
async def get_photo(photo_id: UUID):
    async with unit_of_work() as uow:
        photo = await photo_service.get_by_id(session=uow.session, photo_id=photo_id)
        if photo is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Фотография не найдена")

        return Response(
            content=photo.file_data,
            media_type=photo.mime_type,
            headers={"Content-Disposition": f'inline; filename="{photo.file_name}"'},
        )


@router.post(
    "/products/{product_id}/photos",
    response_model=PhotoResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_admin)],
    summary="Добавить фотографию к продукту",
    description="Загружает фотографию и привязывает ее к выбранному продукту. Метод доступен только администратору.",
)
async def create_photo(product_id: UUID, file: UploadFile = File(...)):
    file_data = await file.read()

    async with unit_of_work() as uow:
        photo = await photo_service.create(
            session=uow.session,
            product_id=product_id,
            file_name=file.filename or "photo",
            mime_type=file.content_type or "application/octet-stream",
            file_size=len(file_data),
            file_data=file_data,
        )
        if photo is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Продукт не найден")
        return photo
