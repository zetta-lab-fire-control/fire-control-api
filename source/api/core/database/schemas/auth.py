from pydantic import BaseModel, Field, ConfigDict


class TokenSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    access_token: str = Field(..., description="The access token.")

    refresh_token: str = Field(..., description="The refresh token.")

    token_type: str = Field("bearer", description="The type of the token.")


class AcessTokenSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    access_token: str = Field(..., description="The access token.")


class RefreshTokenSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    refresh_token: str = Field(..., description="The refresh token.")


class ResetTokenSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    reset_token: str = Field(..., description="The password reset token.")


class PasswordRequestSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: str = Field(..., description="The email of the user.")


class PasswordResetSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    token: str = Field(..., description="The password reset token.")

    new_password: str = Field(..., description="The new password.")
