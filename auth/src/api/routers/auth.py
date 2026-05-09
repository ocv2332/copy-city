from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.security import OAuth2PasswordRequestForm

from api.schemas import LoginRequest, RequestUsers, ResponseUsers, TokenResponse
from api.deps.auth import get_current_user_id, get_token_payload
from core.services.users import UserService
from database.postgres.sessions.uow import unit_of_work
from settings.jwt import settings as jwt_settings

router = APIRouter()
user_service = UserService()
REFRESH_TOKEN_COOKIE_KEY = "refresh_token"


def _set_refresh_cookie(response: Response, refresh_token: str) -> None:
    response.set_cookie(
        key=REFRESH_TOKEN_COOKIE_KEY,
        value=refresh_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=jwt_settings.REFRESH_TOKEN_LIFETIME_SECONDS,
    )

@router.post("/register", response_model=ResponseUsers)
async def register(request: RequestUsers):
    async with unit_of_work() as uow:
        response = await user_service.create_user(session=uow.session, body=request)
        return response


@router.post("/login", response_model=TokenResponse)
async def login(
    request: Request,
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    body = LoginRequest(
        email=form_data.username,
        password=form_data.password,
    )
    async with unit_of_work() as uow:
        result = await user_service.login(
            session=uow.session,
            redis=uow.redis,
            body=body,
            user_agent=request.headers.get("user-agent", "unknown"),
        )
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )
        token_response, refresh_token = result
        _set_refresh_cookie(response, refresh_token)
        return token_response


@router.post("/refresh", response_model=TokenResponse)
async def refresh(request: Request, response: Response):
    refresh_token = request.cookies.get(REFRESH_TOKEN_COOKIE_KEY)
    if refresh_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token is missing",
        )

    async with unit_of_work() as uow:
        result = await user_service.refresh_tokens(
            session=uow.session,
            redis=uow.redis,
            refresh_token_value=refresh_token,
        )
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
            )
        token_response, new_refresh_token = result
        _set_refresh_cookie(response, new_refresh_token)
        return token_response


@router.get("/me", response_model=ResponseUsers)
async def me(
    current_user_id: UUID = Depends(get_current_user_id),
):
    async with unit_of_work() as uow:
        user_model = await UserService.get_user_by_id(session=uow.session, user_id=current_user_id)
        if user_model is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return ResponseUsers.model_validate(user_model)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    request: Request,
    payload: dict = Depends(get_token_payload),
):
    async with unit_of_work() as uow:
        await user_service.logout(
            session=uow.session,
            redis=uow.redis,
            refresh_token_value=request.cookies.get(REFRESH_TOKEN_COOKIE_KEY),
            access_token_jti=payload.get("jti"),
        )
    response = Response(status_code=status.HTTP_204_NO_CONTENT)
    response.delete_cookie(key=REFRESH_TOKEN_COOKIE_KEY)
    return response
