from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.cache.service import CacheService
from core.database import cruds, schemas
from core.security.service import AuthorizationService
from clients.postgres import PostgresClient

router = APIRouter()


@router.post(
    "/firefighters",
    response_model=schemas.UserReadSchema,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(AuthorizationService.get_admin)],
)
def create_firefighter(
    user: schemas.FirefighterCreateSchema, db: Session = Depends(PostgresClient.db)
):

    db_user = cruds.user_crud.create(db=db, instance=user)

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User could not be created"
        )

    CacheService.clear_cache(namespace="users")

    return db_user
