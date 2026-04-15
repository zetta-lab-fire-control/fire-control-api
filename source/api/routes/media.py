from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.orm import Session


from clients.postgres import PostgresClient

from core.database import cruds, schemas

from core.database.models.media import Media

from core.security.service import AuthenticationService

from core.storage.service import MinioService


router = APIRouter()


@router.post(
    "/media",
    response_model=schemas.MediaUploadResponseSchema,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(AuthenticationService.get_current_user)],
)
def create_media(
    media: schemas.MediaCreateSchema, db: Session = Depends(PostgresClient.db)
):

    db_media = cruds.media_crud.create(db=db, instance=media, commit=False)

    if not db_media:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to create media"
        )

    obj_uuid = str(db_media.id)

    obj_name = f"{obj_uuid}.{db_media.extension}"

    obj_url = MinioService().generate_upload_url(
        bucket_name=db_media.bucket, object_name=obj_name, expires_in_minutes=60
    )

    db_media.name = obj_name

    db.commit()

    db.refresh(db_media)

    return schemas.MediaUploadResponseSchema(
        instance_metadata=schemas.MediaReadSchema.model_validate(db_media),
        upload_url=obj_url,
    )


@router.get(
    "/media/{media_id}",
    response_model=schemas.MediaDownloadResponseSchema,
    status_code=status.HTTP_200_OK,
)
def get_media(media_id: str, db: Session = Depends(PostgresClient.db)):

    media: Media | None = cruds.media_crud.read(db=db, id=media_id)

    if not media:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Media not found"
        )

    download_url = MinioService().generate_download_url(
        bucket_name=media.bucket, object_name=media.name
    )

    return schemas.MediaDownloadResponseSchema(
        instance_metadata=schemas.MediaReadSchema.model_validate(media),
        download_url=download_url,
    )
