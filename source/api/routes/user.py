import uuid as uid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.database import cruds, schemas
from clients.postgres import PostgresClient

router = APIRouter()


@router.post(
    "/users", response_model=schemas.UserReadSchema, status_code=status.HTTP_201_CREATED
)
def create_user(
    user: schemas.UserCreateSchema, db: Session = Depends(PostgresClient.db)
):

    db_user = cruds.user_crud.create(db=db, instance=user)

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User could not be created"
        )

    return db_user


@router.get(
    "/users/{user_id}",
    response_model=schemas.UserReadSchema,
    status_code=status.HTTP_200_OK,
)
def read_user(user_id: uid.UUID, db: Session = Depends(PostgresClient.db)):

    db_user = cruds.user_crud.read(db, id=user_id)

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return db_user


@router.put(
    "/users/{user_id}",
    response_model=schemas.UserReadSchema,
    status_code=status.HTTP_200_OK,
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

    return cruds.user_crud.update(db=db, id=user_id, instance=user)


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: uid.UUID, db: Session = Depends(PostgresClient.db)):

    db_user = cruds.user_crud.read(db, id=user_id)

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    cruds.user_crud.delete(db=db, id=user_id)
