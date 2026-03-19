from typing import TypeVar

from pydantic import BaseModel

ModelType = TypeVar("ModelType")


class PaginatedResponse[ModelType](BaseModel):
    total: int
    items: list[ModelType]
