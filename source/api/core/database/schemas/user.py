import uuid

from pydantic import BaseModel, ConfigDict

from core.database.schemas.default import PaginatedResponse


class UserCreateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID

    firstname: str

    lastname: str

    email: str

    telephone: str

    password: str


class UserReadSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID

    firstname: str

    lastname: str

    email: str

    telephone: str


class UserUpdateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID

    firstname: str | None

    lastname: str | None

    email: str | None

    telephone: str | None

    password: str | None


class UserLoginSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: str

    password: str


class UserListSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    users: list[UserReadSchema]


class UserPaginatedResponse(PaginatedResponse[UserReadSchema]):
    pass
