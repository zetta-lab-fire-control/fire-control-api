import uuid as uid

from fastapi import APIRouter, Depends, HTTPException, status
from core.database.schemas.coordinates import CoordinateSchema
from core.database.models.incident import IncidentStatus
from sqlalchemy.orm import Session

from core.database import cruds, schemas
from clients.postgres import PostgresClient

router = APIRouter()


@router.post(
    "/reports",
    response_model=schemas.ReportReadSchema,
    status_code=status.HTTP_201_CREATED,
)
def create_report(
    report: schemas.ReportCreateSchema, db: Session = Depends(PostgresClient.db)
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

    return db_report


@router.get(
    "/reports/{report_id}",
    response_model=schemas.ReportReadSchema,
    status_code=status.HTTP_200_OK,
)
def read_report(report_id: uid.UUID, db: Session = Depends(PostgresClient.db)):

    db_report = cruds.report_crud.read(db, id=report_id)

    if not db_report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Report not found"
        )

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

    return cruds.report_crud.update(db=db, id=report_id, instance=report)


@router.delete("/reports/{report_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_report(report_id: uid.UUID, db: Session = Depends(PostgresClient.db)):

    db_report = cruds.report_crud.read(db, id=report_id)

    if not db_report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Report not found"
        )

    cruds.report_crud.delete(db=db, id=report_id)


@router.get(
    "/reports",
    response_model=schemas.ReportPaginatedResponse,
    status_code=status.HTTP_200_OK,
)
def read_reports(
    skip: int = 0, limit: int = 10, db: Session = Depends(PostgresClient.db)
):
    reports = cruds.report_crud.return_paginated_response(db, skip=skip, limit=limit)
    return schemas.ReportPaginatedResponse(data=reports, skip=skip, limit=limit)
