import uuid as uid

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_cache.decorator import cache
from sqlalchemy.orm import Session


from core.cache.service import CacheService
from core.database.schemas.coordinates import CoordinateSchema
from core.database.enums.incident import IncidentStatus
from core.database.models.occurrence import Occurrence
from core.database import cruds, schemas
from clients.postgres import PostgresClient

router = APIRouter()


@router.post(
    "/reports",
    response_model=schemas.ReportReadSchema,
    status_code=status.HTTP_201_CREATED,
)
def create_report(
    report: schemas.ReportRequestSchema,
    media: list[schemas.MediaReadSchema],
    db: Session = Depends(PostgresClient.db),
):

    point = CoordinateSchema.model_validate(report.location)

    active_occurrence: Occurrence | None = (
        cruds.occurrence_crud.return_occurrence_within_radius(
            db=db, point=point, radius=400
        )
    )

    if not active_occurrence:
        occurrence = schemas.OccurrenceCreateSchema(
            location=point,
            type=report.type,
            intensity=report.intensity,
            status=IncidentStatus.PENDING.value,
        )

        db_occurrence = cruds.occurrence_crud.create(
            db=db, instance=occurrence, commit=False
        )

        if not db_occurrence:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Occurrence could not be created",
            )

    report_data = report.model_dump()

    report_data["occurrence_id"] = (
        active_occurrence.id if active_occurrence else db_occurrence.id
    )

    report_create = schemas.ReportCreateSchema(**report_data)

    db_report = cruds.report_crud.create(db=db, instance=report_create, commit=False)

    if not db_report:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Report could not be created",
        )

    for media_item in media:
        media_report_create = schemas.MediaReportCreateSchema(
            report_id=db_report.id,
            media_id=media_item.id,
        )

        db_media = cruds.media_report_crud.create(
            db=db, instance=media_report_create, commit=False
        )

        if not db_media:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Media could not be created",
            )

    db.commit()

    db.refresh(db_report)

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

    return schemas.ReportReadSchema.model_validate(db_report)


@router.get(
    "/reports",
    response_model=schemas.ReportPaginatedResponse,
    status_code=status.HTTP_200_OK,
)
@cache(expire=60, namespace="reports")
def list_reports(
    skip: int = 0, limit: int = 10, db: Session = Depends(PostgresClient.db)
):

    reports = cruds.report_crud.return_paginated_response(db, skip=skip, limit=limit)

    return schemas.ReportPaginatedResponse(**reports)


@router.get(
    "/reports/{report_id}/media",
    response_model=schemas.MediaReportPaginatedResponse,
    status_code=status.HTTP_200_OK,
)
def list_report_media(
    report_id: uid.UUID,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(PostgresClient.db),
):

    filters = {"report_id": report_id}

    media_reports = cruds.media_report_crud.return_paginated_response(
        db, skip=skip, limit=limit, **filters
    )

    return schemas.MediaReportPaginatedResponse(**media_reports)
