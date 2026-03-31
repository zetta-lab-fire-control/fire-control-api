import uuid as uid

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_cache.decorator import cache
from sqlalchemy.orm import Session

from core.cache.service import CacheService
from core.database.schemas.coordinates import CoordinateSchema
from core.database.models.incident import IncidentStatus
from core.database import cruds, schemas
from clients.postgres import PostgresClient

router = APIRouter(tags=["reports"])


@router.post(
    "/reports",
    response_model=schemas.ReportReadSchema,
    status_code=status.HTTP_201_CREATED,
)
def create_report(
    report: schemas.ReportRequestSchema,
    media: list[schemas.MediaResponseSchema],
    db: Session = Depends(PostgresClient.db),
):
    occurrence_id = None

    point = CoordinateSchema(longitude=report.longitude, latitude=report.latitude)

    active_occurrence = cruds.occurrence_crud.return_occurrence_within_radius(
        db=db, point=point, radius=400
    )

    if active_occurrence:
        occurrence_id = active_occurrence.id

    if not occurrence_id:
        occurrence = schemas.OccurrenceCreateSchema(
            longitude=report.longitude,
            latitude=report.latitude,
            type=report.type,
            status=IncidentStatus.PENDING.value,
            intensity=report.intensity,
        )

        db_occurrence = cruds.occurrence_crud.create(db=db, instance=occurrence)

        occurrence_id = db_occurrence.id

    if not db_occurrence:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Occurrence could not be created",
        )

    report.occurrence_id = occurrence_id

    db_report = cruds.report_crud.create(db=db, instance=report)

    if not db_report:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Report could not be created",
        )

    for media_item in media:
        media_create = schemas.ReportMediaCreateSchema(
            report_id=db_report.id,
            bucket_name=media_item.bucket_name,
            object_name=media_item.object_name,
        )

        db_media = cruds.report_media_crud.create(db=db, instance=media_create)

        if not db_media:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Media could not be created",
            )

    CacheService.clear_cache(namespace="reports")

    return db_report


@router.put(
    "/reports/{report_id}",
    response_model=schemas.ReportReadSchema,
    status_code=status.HTTP_200_OK,
)
def update_report(
    report_id: uid.UUID,
    report: schemas.ReportUpdateSchema,
    db: Session = Depends(PostgresClient.db),
):

    db_report = cruds.report_crud.read(db, id=report_id)

    if not db_report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Report not found"
        )

    CacheService.clear_cache(namespace="reports")

    return cruds.report_crud.update(db=db, id=report_id, instance=report)


@router.delete("/reports/{report_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_report(report_id: uid.UUID, db: Session = Depends(PostgresClient.db)):

    db_report = cruds.report_crud.read(db, id=report_id)

    if not db_report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Report not found"
        )

    cruds.report_crud.delete(db=db, id=report_id)

    CacheService.clear_cache(namespace="reports")


@router.get(
    "/reports/{report_id}",
    response_model=schemas.ReportReadSchema,
    status_code=status.HTTP_200_OK,
)
@cache(expire=60, namespace="reports")
def read_report(report_id: uid.UUID, db: Session = Depends(PostgresClient.db)):

    db_report = cruds.report_crud.read(db, id=report_id)

    if not db_report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Report not found"
        )

    return db_report


@router.get(
    "/reports",
    response_model=schemas.ReportPaginatedResponse,
    status_code=status.HTTP_200_OK,
)
@cache(expire=60, namespace="reports")
def read_reports(
    skip: int = 0, limit: int = 10, db: Session = Depends(PostgresClient.db)
):

    reports = cruds.report_crud.return_paginated_response(db, skip=skip, limit=limit)

    total = cruds.report_crud.count(db)

    return schemas.ReportPaginatedResponse(total=total, items=reports)
