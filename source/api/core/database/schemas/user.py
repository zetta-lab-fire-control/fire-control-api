import uuid

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from core.database.schemas.default import PaginatedResponse


class UserCreateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    firstname: str = Field(..., description="The first name of the user.")

    lastname: str = Field(..., description="The last name of the user.")

    email: str = Field(..., description="The email of the user.")

    telephone: str = Field(..., description="The telephone number of the user.")

    password: str = Field(..., description="The password of the user.")


class UserReadSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID = Field(..., description="The ID of the user.")

    firstname: str = Field(..., description="The first name of the user.")

    lastname: str = Field(..., description="The last name of the user.")

    email: str = Field(..., description="The email of the user.")

    telephone: str = Field(..., description="The telephone number of the user.")


class UserUpdateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    firstname: Optional[str] = Field(None, description="The first name of the user.")

    lastname: Optional[str] = Field(None, description="The last name of the user.")

    email: Optional[str] = Field(None, description="The email of the user.")

    telephone: Optional[str] = Field(
        None, description="The telephone number of the user."
    )

    password: Optional[str] = Field(None, description="The password of the user.")


class UserLoginSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: str = Field(..., description="The email of the user.")

    password: str = Field(..., description="The password of the user.")


class UserAuthSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID = Field(..., description="The ID of the user.")

    role: str = Field(..., description="The role of the user.")


class UserListSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    users: list[UserReadSchema] = Field(..., description="The list of users.")


class UserPaginatedResponse(PaginatedResponse[UserReadSchema]):
    pass
