from sqlalchemy import Column, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from core.database.models.default import DefaultModel


class MediaReport(DefaultModel):
    __tablename__: str = "media_report"

    media_id = Column(
        UUID(as_uuid=True), ForeignKey("media.id", ondelete="CASCADE"), nullable=False
    )

    report_id = Column(
        UUID(as_uuid=True), ForeignKey("reports.id", ondelete="CASCADE"), nullable=False
    )

    media = relationship("Media", back_populates="media_reports")

    report = relationship("Report", back_populates="media")

    __table_args__ = (
        UniqueConstraint("media_id", "report_id", name="uq_media_report"),
    )
