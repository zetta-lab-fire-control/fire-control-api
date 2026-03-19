import uuid as uid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.database import cruds, schemas
from clients.postgres import PostgresClient

router = APIRouter()


@router.post(
    "/occurrences",
    response_model=schemas.OccurrenceReadSchema,
    status_code=status.HTTP_201_CREATED,
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

    return db_occurrence


@router.get(
    "/occurrences/{occurrence_id}",
    response_model=schemas.OccurrenceReadSchema,
    status_code=status.HTTP_200_OK,
)
def read_occurrence(occurrence_id: uid.UUID, db: Session = Depends(PostgresClient.db)):

    db_occurrence = cruds.occurrence_crud.read(db, id=occurrence_id)

    if not db_occurrence:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Occurrence not found"
        )

    return db_occurrence


@router.put(
    "/occurrences/{occurrence_id}",
    response_model=schemas.OccurrenceReadSchema,
    status_code=status.HTTP_200_OK,
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

    return cruds.occurrence_crud.update(db=db, id=occurrence_id, instance=occurrence)


@router.delete("/occurrences/{occurrence_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_occurrence(
    occurrence_id: uid.UUID, db: Session = Depends(PostgresClient.db)
):

    db_occurrence = cruds.occurrence_crud.read(db, id=occurrence_id)

    if not db_occurrence:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Occurrence not found"
        )

    cruds.occurrence_crud.delete(db=db, id=occurrence_id)


@router.get(
    "/occurrences",
    response_model=schemas.OccurrencePaginatedResponse,
    status_code=status.HTTP_200_OK,
)
def read_occurrences(
    skip: int = 0, limit: int = 10, db: Session = Depends(PostgresClient.db)
):

    occurrences = cruds.occurrence_crud.read_all(db, skip=skip, limit=limit)
    total = cruds.occurrence_crud.count(db)

    return schemas.OccurrencePaginatedResponse(total=total, items=occurrences)
