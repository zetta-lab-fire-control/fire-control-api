from core.database.cruds.default import CRUD
from core.database.models import User
from core.database.schemas import UserCreateSchema, UserUpdateSchema
from core.security.service import PasswordService


class UserCRUD(CRUD[User, UserCreateSchema, UserUpdateSchema]):
    def before_create(self, data: dict) -> dict:

        if "password" in data:
            data["password"] = self.hash_password(data["password"])

        return data

    def before_update(self, data: dict) -> dict:

        if "password" in data:
            data["password"] = self.hash_password(data["password"])

        return data

    def password_is_hashed(self, password: str) -> bool:

        prefixes = ("$2b$", "$2a$", "$2y$")

        return password.startswith(prefixes) and len(password) == 60

    def hash_password(self, password: str) -> str:

        password_service = PasswordService()

        if not self.password_is_hashed(password):
            return password_service.hash_password(password)

        return password


user_crud = UserCRUD(User)
