import uuid

from fastapi import APIRouter, status


from core.database import schemas
from core.storage.service import MinioService


router = APIRouter(tags=["media"])


@router.post(
    "/media/upload",
    status_code=status.HTTP_200_OK,
)
def request_media_upload(
    media: schemas.MediaDownloadRequestSchema,
) -> schemas.MediaResponseSchema:

    obj_uuid = str(uuid.uuid4())

    obj_name = f"{obj_uuid}.{media.extension_name}"

    obj_url = MinioService().generate_upload_url(
        bucket_name=media.bucket_name,
        object_name=obj_name,
    )
    return schemas.MediaResponseSchema(
        bucket_name=media.bucket_name,
        object_name=obj_name,
        object_url=obj_url,
    )


@router.post(
    "/media/download",
    status_code=status.HTTP_200_OK,
)
def request_media_download(
    media: schemas.MediaUploadRequestSchema,
) -> schemas.MediaResponseSchema:

    return schemas.MediaResponseSchema(
        bucket_name=media.bucket_name,
        object_name=media.object_name,
        object_url=MinioService().generate_download_url(
            bucket_name=media.bucket_name,
            object_name=media.object_name,
        ),
    )
