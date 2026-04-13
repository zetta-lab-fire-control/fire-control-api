import os

from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from clients.postgres import PostgresClient
from core.database import cruds, schemas
from core.cache.service import CacheService

load_dotenv()


class Data:
    SECRET_KEY: str | None = os.getenv("SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int | None = (
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"),
        15,
    )
    REFRESH_TOKEN_EXPIRE_HOURS: int | None = (
        os.getenv("REFRESH_TOKEN_EXPIRE_HOURS"),
        24,
    )
    PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")
    AUTH_SCHEME = OAuth2PasswordBearer(tokenUrl="token")
    AUTH_SCHEME_OPTIONAL = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)


class PasswordService:
    def hash_password(self, password: str) -> str:

        return Data.PWD_CONTEXT.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:

        return Data.PWD_CONTEXT.verify(plain_password, hashed_password)


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
