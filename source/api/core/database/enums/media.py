from enum import StrEnum


class MediaExtension(StrEnum):
    PNG = "png"

    MP4 = "mp4"

    PDF = "pdf"

    CSV = "csv"


class MediaType(StrEnum):
    IMAGE = "image"

    VIDEO = "video"

    DOCUMENT = "document"


class Bucket(StrEnum):
    REPORTS = "reports"
