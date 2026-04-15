from typing import Optional
import uuid as uid

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi_cache.decorator import cache
from sqlalchemy.orm import Session

from clients.postgres import PostgresClient
from core.database import cruds, schemas
from core.cache.service import CacheService
from core.database.enums.incident import IncidentStatus
from core.database.services.ocurrence import OccurrenceService
from core.security.service import AuthorizationService


router = APIRouter()


@router.post(
    "/occurrences",
    response_model=schemas.OccurrenceReadSchema,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(AuthorizationService.get_admin_or_firefighter)],
)
def create_occurrence(
    occurrence: schemas.OccurrenceCreateSchema, db: Session = Depends(PostgresClient.db)
):

    db_occurrence = cruds.occurrence_crud.create(db=db, instance=occurrence)

    if not db_occurrence:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Occurrence could not be created",
        )

    CacheService.clear_cache(namespace="occurrences")

    return db_occurrence


@router.put(
    "/occurrences/{occurrence_id}",
    response_model=schemas.OccurrenceReadSchema,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(AuthorizationService.get_admin_or_firefighter)],
)
def update_occurrence(
    occurrence_id: uid.UUID,
    occurrence: schemas.OccurrenceUpdateSchema,
    db: Session = Depends(PostgresClient.db),
):

    db_occurrence = cruds.occurrence_crud.read(db, id=occurrence_id)

    if not db_occurrence:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Occurrence not found"
        )

    CacheService.clear_cache(namespace="occurrences")

    return cruds.occurrence_crud.update(db=db, id=occurrence_id, instance=occurrence)


@router.delete(
    "/occurrences/{occurrence_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(AuthorizationService.get_admin_or_firefighter)],
)
def delete_occurrence(
    occurrence_id: uid.UUID, db: Session = Depends(PostgresClient.db)
):

    db_occurrence = cruds.occurrence_crud.read(db, id=occurrence_id)

    if not db_occurrence:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Occurrence not found"
        )

    cruds.occurrence_crud.delete(db=db, id=occurrence_id)

    CacheService.clear_cache(namespace="occurrences")


@router.get(
    "/occurrences/{occurrence_id}",
    response_model=schemas.OccurrenceReadSchema,
    status_code=status.HTTP_200_OK,
)
@cache(expire=60, namespace="occurrences")
def read_occurrence(occurrence_id: uid.UUID, db: Session = Depends(PostgresClient.db)):

    db_occurrence = cruds.occurrence_crud.read(db, id=occurrence_id)

    if not db_occurrence:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Occurrence not found"
        )

    return schemas.OccurrenceReadSchema.model_validate(db_occurrence)


@router.get(
    "/occurrences",
    response_model=schemas.OccurrencePaginatedResponse,
    status_code=status.HTTP_200_OK,
)
@cache(expire=180, namespace="occurrences")
def list_occurrences(
    status: Optional[IncidentStatus] = None,
    city: Optional[str] = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(PostgresClient.db),
):

    filters = {
        "city": city if city else None,
        "status": status if status else None,
    }

    occurrences = cruds.occurrence_crud.return_paginated_response(
        db=db, skip=skip, limit=limit, **filters
    )

    return schemas.OccurrencePaginatedResponse(**occurrences)


@router.get(
    "/occurrences/indicators/history",
    response_model=schemas.OccurrenceHistorySchema,
    status_code=status.HTTP_200_OK,
)
@cache(expire=60, namespace="occurrences")
def get_history(
    start_date: datetime = Query(
        ..., description="Start date in ISO format (YYYY-MM-DD)"
    ),
    end_date: datetime = Query(..., description="End date in ISO format (YYYY-MM-DD)"),
    db: Session = Depends(PostgresClient.db),
):
    occurrence_service = OccurrenceService()
    indicators = occurrence_service.get_history_indicators(db, start_date, end_date)
    return indicators


@router.get(
    "/occurrences/indicators/operational",
    response_model=schemas.OccurrenceOperationalIndicatorsSchema,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(AuthorizationService.get_admin_or_firefighter)],
)
@cache(expire=60, namespace="occurrences")
def get_operational_indicators(
    city: str = Query(..., description="City name for which to retrieve indicators"),
    target_date: datetime = Query(
        ..., description="Target date in ISO format (YYYY-MM-DD)"
    ),
    db: Session = Depends(PostgresClient.db),
):
    occurrence_service = OccurrenceService()
    indicators = occurrence_service.get_operational_indicators(
        db, city=city, target_date=target_date
    )
    return indicators


@router.get(
    "/occurrences/indicators/public",
    response_model=schemas.OccurrencePublicIndicatorsSchema,
    status_code=status.HTTP_200_OK,
)
@cache(expire=60, namespace="occurrences")
def get_public_indicators(db: Session = Depends(PostgresClient.db)):
    occurrence_service = OccurrenceService()
    indicators = occurrence_service.get_public_indicators(db)
    return indicators
