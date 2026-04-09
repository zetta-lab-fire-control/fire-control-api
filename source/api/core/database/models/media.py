from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from core.database.models.default import DefaultModel


class Media(DefaultModel):
    __tablename__ = "media"

    bucket = Column(String, nullable=True)

    name = Column(String, nullable=True)

    type = Column(String, nullable=True)

    size = Column(Integer, nullable=True)

    extension = Column(String, nullable=True)

    url = Column(String, nullable=True)

    description = Column(String, nullable=True)

    media_reports = relationship("MediaReport", back_populates="media")
