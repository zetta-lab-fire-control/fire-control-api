from core.database.cruds.default import CRUD
from core.database.models import User
from core.database.schemas import UserCreateSchema, UserUpdateSchema


class UserCRUD(CRUD[User, UserCreateSchema, UserUpdateSchema]):
    def before_create(self, data: dict) -> dict:

        data["password"] = self.hash_password(data["password"])

        return data

    def before_update(self, data: dict) -> dict:

        if "password" in data:
            data["password"] = self.hash_password(data["password"])

        return data

    def hash_password(self, password: str) -> str:

        # Implement password hashing logic

        return password


user_crud = UserCRUD(User)
