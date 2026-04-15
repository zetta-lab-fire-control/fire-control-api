import pytest

from unittest.mock import AsyncMock, patch


@pytest.fixture(scope="function")
@patch(
    "routes.auth.CacheService.is_token_blocked",
    return_value=False,
    new_callable=AsyncMock,
)
def report(mock_is_token_blocked, auth_client, media, report_data):

    response = auth_client.post(
        "/reports",
        json={"report": report_data, "media": [media["instance_metadata"]]},
    )

    return response.json()
