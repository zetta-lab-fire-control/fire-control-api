from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from clients.postgres import PostgresClient
from core.database import cruds, schemas
from core.cache.service import CacheService
from core.security.service import (
    Data,
    AuthenticationService,
    TokenService,
    PasswordService,
)


router = APIRouter()


@router.post(
    "/login", response_model=schemas.TokenSchema, status_code=status.HTTP_200_OK
)
def login(
    data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(PostgresClient.db),
):

    filter = {
        "email": data.username,
    }

    user = cruds.user_crud.read_by(db, **filter)
    password = (
        PasswordService().verify_password(data.password, user.password)
        if user
        else False
    )

    if not user or not password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = TokenService().create_access_token(data={"sub": str(user.id)})
    refresh_token = TokenService().create_refresh_token(data={"sub": str(user.id)})

    return schemas.TokenSchema(access_token=token, refresh_token=refresh_token)


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(
    token: str = Depends(Data.AUTH_SCHEME),
    current_user: schemas.UserAuthSchema = Depends(
        AuthenticationService.get_current_user
    ),
):
    payload = TokenService().decode_access_token(token)

    if payload and "exp" in payload:
        await CacheService.block_token(token, payload["exp"])

    return {"message": "User logged out successfully."}


@router.post(
    "/refresh", response_model=schemas.TokenSchema, status_code=status.HTTP_200_OK
)
async def refresh_token(
    refresh_token: schemas.RefreshTokenSchema, db: Session = Depends(PostgresClient.db)
):
    payload = TokenService().decode_access_token(refresh_token.refresh_token)

    if not payload or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token invalid or expired.",
        )

    if await CacheService.is_token_blocked(refresh_token.refresh_token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session terminated prematurely.",
        )

    user_id = payload.get("sub")

    user = cruds.user_crud.read(db, id=user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found.",
        )

    new_access_token = TokenService().create_access_token(data={"sub": str(user.id)})
    new_refresh_token = TokenService().create_refresh_token(data={"sub": str(user.id)})

    await CacheService.block_token(refresh_token.refresh_token, payload["exp"])

    return schemas.TokenSchema(
        access_token=new_access_token,
        refresh_token=new_refresh_token,
        token_type="bearer",
    )


@router.post(
    "/password-request",
    response_model=schemas.ResetTokenSchema,
    status_code=status.HTTP_200_OK,
)
def request_password(
    data: schemas.PasswordRequestSchema, db: Session = Depends(PostgresClient.db)
):

    filter = {
        "email": data.email,
    }

    user = cruds.user_crud.read_by(db, **filter)

    if user:
        token_service = TokenService()

        reset_token = token_service.create_reset_token(data={"sub": str(user.id)})

    if not user:
        fake_token = token_service.create_reset_token(data={"sub": "fake_user_id"})

    return (
        schemas.ResetTokenSchema(reset_token=reset_token)
        if user
        else schemas.ResetTokenSchema(reset_token=fake_token)
    )


@router.post("/password-reset", status_code=status.HTTP_200_OK)
async def reset_password(
    data: schemas.PasswordResetSchema, db: Session = Depends(PostgresClient.db)
):
    if await CacheService.is_token_blocked(data.token):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token already used or invalid.",
        )

    token_service = TokenService()

    payload = token_service.decode_access_token(data.token)

    if not payload or payload.get("type") != "reset":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token already used or invalid.",
        )

    user = cruds.user_crud.read(db, id=payload.get("sub"))

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )

    password_service = PasswordService()

    hashed_password = password_service.hash_password(data.new_password)

    user_data = schemas.UserUpdateSchema(password=hashed_password)

    cruds.user_crud.update(db, id=user.id, instance=user_data)

    await CacheService.block_token(data.token, payload["exp"])

    return {"message": "Password reset successfully."}
