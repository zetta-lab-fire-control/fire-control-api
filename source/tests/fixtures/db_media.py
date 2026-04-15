import pytest
from unittest.mock import AsyncMock, patch


@pytest.fixture(scope="function")
@patch(
    "routes.auth.CacheService.is_token_blocked",
    return_value=False,
    new_callable=AsyncMock,
)
def media(mock_is_token_blocked, auth_client, media_data):

    response = auth_client.post(
        "/media",
        json=media_data,
    )

    return response.json()
