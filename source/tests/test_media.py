from unittest.mock import patch


def test_create_media(media):

    assert "instance_metadata" in media


def test_get_media(client, media):

    media_id = media["instance_metadata"]["id"]

    response = client.get(f"/media/{media_id}")

    assert response.status_code == 200


def test_create_media_return_not_db_occurrence(client):

    media = {
        "bucket": "reports",
        "extension": "png",
        "type": "image",
        "size": 85,
        "description": "test image",
    }

    mock_media_create_response = "api.routes.media.cruds.media_crud.create"

    with patch(mock_media_create_response, return_value=None):
        response = client.post(
            "/media",
            json=media,
        )

    assert response.status_code == 400


def test_get_media_return_not_db_occurrence(client):

    media_id = "00000000-0000-0000-0000-000000000000"

    response = client.get(f"/media/{media_id}")

    assert response.status_code == 404
