from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from core.database.models.default import DefaultModel


class ReportMedia(DefaultModel):
    __tablename__ = "reports-media"

    report_id = Column(UUID(as_uuid=True), ForeignKey("reports.id"), nullable=True)

    bucket_name = Column(String, nullable=True)

    object_name = Column(String, nullable=True)

    report = relationship("Report", back_populates="media")
