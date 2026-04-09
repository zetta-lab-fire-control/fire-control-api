import uuid as uid


from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_cache.decorator import cache
from sqlalchemy.orm import Session

from core.cache.service import CacheService
from core.database import cruds, schemas
from clients.postgres import PostgresClient

router = APIRouter()


@router.post(
    "/users",
    response_model=schemas.UserReadSchema,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "User could not be created"},
    },
)
def create_user(
    user: schemas.UserCreateSchema, db: Session = Depends(PostgresClient.db)
):

    db_user = cruds.user_crud.create(db=db, instance=user)

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User could not be created"
        )

    CacheService.clear_cache(namespace="users")

    return db_user


@router.put(
    "/users/{user_id}",
    response_model=schemas.UserReadSchema,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "User not found"},
    },
)
def update_user(
    user_id: uid.UUID,
    user: schemas.UserUpdateSchema,
    db: Session = Depends(PostgresClient.db),
):

    db_user = cruds.user_crud.read(db, id=user_id)

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    CacheService.clear_cache(namespace="users")

    return cruds.user_crud.update(db=db, id=user_id, instance=user)


@router.delete(
    "/users/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "User not found"},
    },
)
def delete_user(user_id: uid.UUID, db: Session = Depends(PostgresClient.db)):

    db_user = cruds.user_crud.read(db, id=user_id)

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    cruds.user_crud.delete(db=db, id=user_id)

    CacheService.clear_cache(namespace="users")


@router.get(
    "/users/{user_id}",
    response_model=schemas.UserReadSchema,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "User not found"},
    },
)
@cache(expire=60, namespace="users")
def read_user(user_id: uid.UUID, db: Session = Depends(PostgresClient.db)):

    db_user = cruds.user_crud.read(db, id=user_id)

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return db_user


@router.get(
    "/users",
    response_model=schemas.UserPaginatedResponse,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Users not found"},
    },
)
@cache(expire=60, namespace="users")
def list_users(
    skip: int = 0, limit: int = 10, db: Session = Depends(PostgresClient.db)
):

    users = cruds.user_crud.return_paginated_response(db=db, skip=skip, limit=limit)

    return schemas.UserPaginatedResponse(**users)
