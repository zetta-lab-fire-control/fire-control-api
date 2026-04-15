from unittest.mock import AsyncMock, patch


def test_create_user(user):

    assert "id" in user


def test_create_user_returns_400(client):

    user = {
        "firstname": "user",
        "lastname": "test",
        "email": "test@example.com",
        "telephone": "123456789",
        "password": "securepassword",
    }

    mock_target = "api.routes.user.cruds.user_crud.create"

    with patch(mock_target, return_value=None):
        response = client.post("/users", json=user)

    assert response.status_code == 400

    assert response.json() == {"detail": "User could not be created"}


@patch(
    "routes.auth.CacheService.is_token_blocked",
    return_value=False,
    new_callable=AsyncMock,
)
def test_update_user(mock_is_token_blocked, auth_client, user):

    user_id = user["id"]

    response = auth_client.put(
        f"/users/{user_id}",
        json={
            "firstname": "updated",
            "lastname": "user",
            "email": "updateduser@example.com",
            "telephone": "987654321",
            "password": "newsecurepassword",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == user_id


@patch(
    "routes.auth.CacheService.is_token_blocked",
    return_value=False,
    new_callable=AsyncMock,
)
def test_delete_user(mock_is_token_blocked, auth_client, user):

    user_id = user["id"]

    response = auth_client.delete(f"/users/{user_id}")

    assert response.status_code == 204


@patch(
    "routes.auth.CacheService.is_token_blocked",
    return_value=False,
    new_callable=AsyncMock,
)
def test_get_user(mock_is_token_blocked, auth_client, user):

    user_id = user["id"]

    response = auth_client.get(f"/users/{user_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == user_id


def test_list_users(mocked_admin_client):

    response = mocked_admin_client.get("/users")

    assert response.status_code == 200
