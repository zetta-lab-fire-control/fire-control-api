import uuid

from datetime import datetime, timezone
from sqlalchemy import Column, DateTime
from sqlalchemy.dialects.postgresql import UUID

from clients.postgres import PostgresClient


class CRUDMixin:
    def create(self, db):

        db.add(self)

        db.commit()

        db.refresh(self)

        return self

    def update(self, db, **kwargs):

        for key, value in kwargs.items():
            setattr(self, key, value)

        db.commit()

        db.refresh(self)

        return self

    def delete(self, db):

        db.delete(self)

        db.commit()


class DefaultModel(PostgresClient.Base, CRUDMixin):
    __abstract__ = True

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    updated_at = Column(
        DateTime(timezone=True), onupdate=lambda: datetime.now(timezone.utc)
    )
