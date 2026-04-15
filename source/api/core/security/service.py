import bcrypt
import os

from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from clients.postgres import PostgresClient
from core.cache.service import CacheService
from core.database import cruds, schemas
from core.database.enums.roles import Role
from core.database.models.report import Report


load_dotenv()


class Data:
    SECRET_KEY: str | None = os.getenv("API_SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 15))
    REFRESH_TOKEN_EXPIRE_HOURS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_HOURS", 24))
    AUTH_SCHEME = OAuth2PasswordBearer(tokenUrl="login")
    AUTH_SCHEME_OPTIONAL = OAuth2PasswordBearer(tokenUrl="login", auto_error=False)


class PasswordService:
    def hash_password(self, password: str) -> str:

        pwd_bytes = password.encode("utf-8")

        salt = bcrypt.gensalt()

        hashed_bytes = bcrypt.hashpw(pwd_bytes, salt)

        return hashed_bytes.decode("utf-8")

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:

        plain_bytes = plain_password.encode("utf-8")

        hashed_bytes = hashed_password.encode("utf-8")

        return bcrypt.checkpw(plain_bytes, hashed_bytes)


class TokenService:
    def create_access_token(self, data: dict) -> str:

        to_encode = data.copy()

        expire = datetime.now(timezone.utc) + timedelta(
            minutes=Data.ACCESS_TOKEN_EXPIRE_MINUTES
        )

        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(to_encode, Data.SECRET_KEY, algorithm=Data.ALGORITHM)

        return encoded_jwt

    def create_refresh_token(self, data: dict) -> str:

        to_encode = data.copy()

        expire = datetime.now(timezone.utc) + timedelta(
            hours=Data.REFRESH_TOKEN_EXPIRE_HOURS
        )

        to_encode.update({"exp": expire, "type": "refresh"})

        encoded_jwt = jwt.encode(to_encode, Data.SECRET_KEY, algorithm=Data.ALGORITHM)

        return encoded_jwt

    def create_reset_token(self, data: dict) -> str:

        to_encode = data.copy()

        expire = datetime.now(timezone.utc) + timedelta(hours=1)

        to_encode.update({"exp": expire, "type": "reset"})

        encoded_jwt = jwt.encode(to_encode, Data.SECRET_KEY, algorithm=Data.ALGORITHM)

        return encoded_jwt

    def decode_access_token(self, token: str) -> dict:

        try:
            payload = jwt.decode(token, Data.SECRET_KEY, algorithms=[Data.ALGORITHM])

            return payload

        except JWTError:
            return None


class AuthenticationService:
    @classmethod
    async def credentials_exception(cls):

        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    @classmethod
    async def get_current_user(
        cls,
        token: str = Depends(Data.AUTH_SCHEME),
        db: Session = Depends(PostgresClient.db),
    ) -> schemas.UserAuthSchema:

        token_service = TokenService()

        payload = token_service.decode_access_token(token)

        if payload is None:
            raise await cls.credentials_exception()

        if payload.get("type") == "refresh":
            raise await cls.credentials_exception()

        is_blocked = await CacheService.is_token_blocked(token)

        if is_blocked:
            raise await cls.credentials_exception()

        user_id: str = payload.get("sub")

        if user_id is None:
            raise await cls.credentials_exception()

        user = cruds.user_crud.read(db, id=user_id)

        if user is None:
            raise await cls.credentials_exception()

        return schemas.UserAuthSchema(id=user.id, role=user.role)


class AuthorizationService:
    @classmethod
    async def authorization_exception(cls):

        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action",
        )

    @classmethod
    async def instance_not_found_exception(cls, resource_name: str):

        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{resource_name} not found",
        )

    @classmethod
    async def get_admin_or_firefighter(
        cls,
        current_user: schemas.UserAuthSchema = Depends(
            AuthenticationService.get_current_user
        ),
    ) -> schemas.UserAuthSchema:

        authorized_roles = [Role.ADMIN.value, Role.FIREFIGHTER.value]

        user_role = current_user.role

        is_admin_or_firefighter = [
            user_role.lower() == role.lower() for role in authorized_roles
        ]

        is_authorized = any(is_admin_or_firefighter)

        if not is_authorized:
            raise await cls.authorization_exception()

        return current_user

    @classmethod
    async def get_user_instance_owner_or_admin(
        cls,
        user_id: str,
        current_user: schemas.UserAuthSchema = Depends(
            AuthenticationService.get_current_user
        ),
    ) -> schemas.UserAuthSchema:

        is_owner = str(user_id) == str(current_user.id)

        is_admin = current_user.role.lower() == Role.ADMIN.value.lower()

        if not is_owner and not is_admin:
            raise await cls.authorization_exception()

        return current_user

    @classmethod
    async def get_report_instance_owner_or_admin(
        cls,
        report_id: str,
        current_user: schemas.UserAuthSchema = Depends(
            AuthenticationService.get_current_user
        ),
        db: Session = Depends(PostgresClient.db),
    ) -> schemas.UserAuthSchema:

        report: Report | None = cruds.report_crud.read(db, id=report_id)

        if report is None:
            raise await cls.instance_not_found_exception("Report")

        is_owner = str(report.user_id) == str(current_user.id)

        is_admin = current_user.role.upper() == Role.ADMIN.value

        if not is_owner and not is_admin:
            raise await cls.authorization_exception()

        return current_user
