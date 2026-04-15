from unittest.mock import AsyncMock, patch


def test_create_media(media):

    assert "instance_metadata" in media


@patch(
    "routes.auth.CacheService.is_token_blocked",
    return_value=False,
    new_callable=AsyncMock,
)
@patch("routes.media.cruds.media_crud.create", return_value=None)
def test_create_media_return_not_db_occurrence(
    mock_create, mock_is_token_blocked, auth_client, media_data
):

    response = auth_client.post(
        "/media",
        json=media_data,
    )

    assert response.status_code == 400


def test_get_media(client, media):

    media_id = media["instance_metadata"]["id"]

    response = client.get(f"/media/{media_id}")

    assert response.status_code == 200


def test_get_media_return_not_db_media(client):

    media_id = "00000000-0000-0000-0000-000000000000"

    response = client.get(f"/media/{media_id}")

    assert response.status_code == 404
