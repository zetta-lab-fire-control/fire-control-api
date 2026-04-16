import pytest

from fastapi.testclient import TestClient

from api.app import app
from api.clients.postgres import PostgresClient

from core.database import schemas
from core.database.enums.roles import Role
from core.security.service import AuthenticationService


@pytest.fixture(scope="function")
def client(db_session):

    def _get_db_session_():

        yield db_session

    app.dependency_overrides[PostgresClient.db] = _get_db_session_

    try:
        with TestClient(app) as client:
            yield client

    finally:
        # app.dependency_overrides.clear()
        app.dependency_overrides = {}


@pytest.fixture(scope="function")
def auth_client(client, user_access_token):

    client.headers = {**client.headers, "Authorization": f"Bearer {user_access_token}"}

    return client


@pytest.fixture(scope="function")
def admin_client(client, admin_access_token):

    client.headers = {**client.headers, "Authorization": f"Bearer {admin_access_token}"}

    return client


@pytest.fixture(scope="function")
def mocked_admin_client(client, admin):

    async def mock_get_current_user():
        return schemas.UserAuthSchema(id=admin["id"], role=Role.ADMIN.value)

    app.dependency_overrides[AuthenticationService.get_current_user] = (
        mock_get_current_user
    )

    try:
        yield client

    finally:
        app.dependency_overrides.pop(AuthenticationService.get_current_user, None)
        # app.dependency_overrides = {}
        # app.dependency_overrides.clear()
