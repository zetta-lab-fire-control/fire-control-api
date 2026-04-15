import pytest

from api.core.security.service import TokenService

from api.core.database.cruds import user_crud
from api.core.database.schemas.user import AdminCreateSchema


@pytest.fixture(scope="function")
def admin(admin_data, db_session):

    admin_create_schema = AdminCreateSchema(**admin_data)

    db_admin = user_crud.create(db_session, instance=admin_create_schema)

    yield {
        "id": str(db_admin.id),
    }


@pytest.fixture(scope="function")
def admin_credentials(admin_data, admin):
    return {"username": admin_data["email"], "password": admin_data["password"]}


@pytest.fixture(scope="function")
def admin_access_token(admin):
    access_token = TokenService().create_access_token(data={"sub": admin["id"]})
    return access_token


@pytest.fixture(scope="function")
def admin_reset_token(admin):
    reset_token = TokenService().create_reset_token(data={"sub": admin["id"]})
    return reset_token


@pytest.fixture(scope="function")
def admin_refresh_token(admin):
    refresh_token = TokenService().create_refresh_token(data={"sub": admin["id"]})
    return refresh_token
