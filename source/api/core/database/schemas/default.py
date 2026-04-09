from typing import TypeVar

from pydantic import BaseModel, Field

ModelType = TypeVar("ModelType")


class PaginatedResponse[ModelType](BaseModel):
    total: int = Field(..., description="Total number of items available")

    items: list[ModelType] = Field(
        ..., description="List of items for the current page"
    )
