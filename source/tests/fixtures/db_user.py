import pytest

from api.core.security.service import TokenService


@pytest.fixture(scope="function")
def user(client, user_data):

    response = client.post(
        "/users",
        json=user_data,
        headers={},
    )

    data = response.json()

    if "id" not in data:
        pytest.fail(f"Failed to create test user: {data}")

    return data


@pytest.fixture(scope="function")
def user_credentials(user_data):
    return {"username": user_data["email"], "password": user_data["password"]}


@pytest.fixture(scope="function")
def user_access_token(user):
    access_token = TokenService().create_access_token(data={"sub": user["id"]})
    return access_token


@pytest.fixture(scope="function")
def user_reset_token(user):
    reset_token = TokenService().create_reset_token(data={"sub": user["id"]})
    return reset_token


@pytest.fixture(scope="function")
def user_refresh_token(user):
    refresh_token = TokenService().create_refresh_token(data={"sub": user["id"]})
    return refresh_token
