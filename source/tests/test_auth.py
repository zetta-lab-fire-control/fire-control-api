from unittest.mock import patch


def test_login(auth_client, user_credentials):
    response = auth_client.post("/login", data=user_credentials)
    assert response.status_code == 200


def test_login_return_unauthorized(client, user_credentials):
    response = client.post("/login", data=user_credentials)
    assert response.status_code == 401


def test_logout(auth_client):
    response = auth_client.post("/logout")
    assert response.status_code == 200


def test_password_request(client, user):
    response = client.post("/password-request", json={"email": user["email"]})
    assert response.status_code == 200


def test_password_request_not_user(client):
    response = client.post(
        "/password-request", json={"email": "nonexistent@example.com"}
    )
    assert response.status_code == 200


@patch("routes.auth.CacheService.block_token", return_value=None)
@patch("routes.auth.CacheService.is_token_blocked", return_value=False)
def test_reset_password(mock_is_blocked, mock_block_token, client, user_reset_token):

    response = client.post(
        "/password-reset",
        json={"token": user_reset_token, "new_password": "new_secure_password"},
    )

    assert response.status_code == 200


@patch("routes.auth.CacheService.block_token", return_value=None)
@patch("routes.auth.CacheService.is_token_blocked", return_value=True)
def test_reset_password_blocked_token(
    mock_is_blocked, mock_block_token, client, user_reset_token
):

    response = client.post(
        "/password-reset",
        json={"token": user_reset_token, "new_password": "new_secure_password"},
    )

    assert response.status_code == 400


@patch("routes.auth.CacheService.block_token", return_value=None)
@patch("routes.auth.TokenService.decode_access_token", return_value=None)
@patch("routes.auth.CacheService.is_token_blocked", return_value=False)
def test_reset_password_return_none_payload(
    mock_is_blocked, mock_decode_token, mock_block_token, client, user_reset_token
):

    response = client.post(
        "/password-reset",
        json={"token": user_reset_token, "new_password": "new_secure_password"},
    )

    assert response.status_code == 400


@patch("routes.auth.CacheService.block_token", return_value=None)
@patch("routes.auth.cruds.user_crud.read", return_value=None)
@patch("routes.auth.CacheService.is_token_blocked", return_value=False)
def test_reset_password_return_none_user(
    mock_is_blocked, mock_read_user, mock_block_token, client, user_reset_token
):

    response = client.post(
        "/password-reset",
        json={"token": user_reset_token, "new_password": "new_secure_password"},
    )

    assert response.status_code == 404


@patch("routes.auth.CacheService.block_token", return_value=None)
@patch("routes.auth.CacheService.is_token_blocked", return_value=False)
def test_refresh_token(mock_is_blocked, mock_block_token, client, user_refresh_token):

    response = client.post("/refresh", json={"refresh_token": user_refresh_token})

    assert response.status_code == 200


@patch("routes.auth.CacheService.block_token", return_value=None)
@patch("routes.auth.TokenService.decode_access_token", return_value=None)
@patch("routes.auth.CacheService.is_token_blocked", return_value=False)
def test_refresh_token_return_none_payload(
    mock_is_blocked, mock_decode_token, mock_block_token, client, user_refresh_token
):

    response = client.post("/refresh", json={"refresh_token": user_refresh_token})

    assert response.status_code == 401


@patch("routes.auth.CacheService.block_token", return_value=None)
@patch("routes.auth.CacheService.is_token_blocked", return_value=True)
def test_refresh_token_blocked_token(
    mock_is_blocked, mock_block_token, client, user_refresh_token
):

    response = client.post("/refresh", json={"refresh_token": user_refresh_token})

    assert response.status_code == 401


@patch("routes.auth.CacheService.block_token", return_value=None)
@patch("routes.auth.cruds.user_crud.read", return_value=None)
@patch("routes.auth.CacheService.is_token_blocked", return_value=False)
def test_refresh_token_return_none_user(
    mock_is_blocked, mock_read_user, mock_block_token, client, user_refresh_token
):

    response = client.post("/refresh", json={"refresh_token": user_refresh_token})

    assert response.status_code == 401
