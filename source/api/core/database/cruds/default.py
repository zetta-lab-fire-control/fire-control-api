from typing import Any, TypeVar

from pydantic import BaseModel
from sqlalchemy.orm import Session


ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUD[ModelType, CreateSchemaType: BaseModel, UpdateSchemaType: BaseModel]:
    def __init__(self, model: type[ModelType]):

        self.model = model

    def flush(self, db: Session, instance: CreateSchemaType) -> ModelType:

        db_obj = self.model(instance.model_dump())

        db.add(db_obj)

        db.flush()

    def before_create(self, data: dict) -> dict:

        return data

    def create(
        self, db: Session, instance: CreateSchemaType, commit: bool = True
    ) -> ModelType:

        data = self.before_create(instance.model_dump())

        db_obj = self.model(**data)

        db.add(db_obj)

        if commit:
            db.commit()

            db.refresh(db_obj)

        else:
            db.flush()

        return db_obj

    def read(self, db: Session, id: Any) -> ModelType | None:

        query = db.query(self.model).filter(self.model.id == id)

        return query.first()

    def read_by(self, db: Session, **filters) -> ModelType | None:

        query = db.query(self.model)

        for key, value in filters.items():
            query = query.filter(getattr(self.model, key) == value)

        return query.first()

    def before_update(self, data: dict) -> dict:

        return data

    def update(
        self, db: Session, id: Any, instance: UpdateSchemaType
    ) -> ModelType | None:

        db_obj = db.get(self.model, id)

        if not db_obj:
            return None

        data = self.before_update(instance.model_dump(exclude_unset=True))

        for key, value in data.items():
            setattr(db_obj, key, value)

        db.commit()

        db.refresh(db_obj)

        return db_obj

    def delete(self, db: Session, id: Any) -> Any:

        db_obj = db.get(self.model, id)

        if not db_obj:
            return None

        db.delete(db_obj)

        db.commit()

        return id

    def list(
        self, db: Session, skip: int = 0, limit: int = 100, **filters
    ) -> list[ModelType]:

        query = db.query(self.model)

        for key, value in filters.items():
            if value is not None:
                query = query.filter(getattr(self.model, key) == value)

        return query.offset(skip).limit(limit).all()

    def count(self, db: Session, **filters) -> int:

        query = db.query(self.model)

        for key, value in filters.items():
            if value is not None:
                query = query.filter(getattr(self.model, key) == value)

        return query.count()

    def return_paginated_response(
        self, db: Session, skip: int = 0, limit: int = 100, **filters
    ) -> dict[str, Any]:

        return {
            "total": self.count(db, **filters),
            "items": self.list(db, skip=skip, limit=limit, **filters),
        }
