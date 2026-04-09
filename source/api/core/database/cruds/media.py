from core.database.cruds.default import CRUD
from core.database.models import Media
from core.database.schemas import MediaCreateSchema, MediaUpdateSchema


class MediaCRUD(CRUD[Media, MediaCreateSchema, MediaUpdateSchema]):
    pass


media_crud = MediaCRUD(Media)
