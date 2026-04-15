from unittest.mock import AsyncMock, patch


def test_create_report(report):

    assert "id" in report


@patch(
    "routes.auth.CacheService.is_token_blocked",
    return_value=False,
    new_callable=AsyncMock,
)
def test_create_report_return_not_db_occurrence(
    mock_is_token_blocked, auth_client, user, media
):

    report = {
        "user_id": user["id"],
        "location": {"longitude": 0.0, "latitude": 0.0},
        "type": "forest_fire",
        "intensity": "high",
    }

    mock_active_occurrence_target = (
        "api.routes.report.cruds.occurrence_crud.return_occurrence_within_radius"
    )
    mock_db_occurrence_target = "api.routes.report.cruds.occurrence_crud.create"

    with patch(mock_active_occurrence_target, return_value=None):
        with patch(mock_db_occurrence_target, return_value=None):
            response = auth_client.post(
                "/reports",
                json={"report": report, "media": [media["instance_metadata"]]},
            )

    assert response.status_code == 400


@patch(
    "routes.auth.CacheService.is_token_blocked",
    return_value=False,
    new_callable=AsyncMock,
)
def test_create_report_return_not_db_report(
    mock_is_token_blocked, auth_client, user, media
):

    report = {
        "user_id": user["id"],
        "location": {"longitude": 0.0, "latitude": 0.0},
        "type": "forest_fire",
        "intensity": "high",
    }

    mock_target = "api.routes.report.cruds.report_crud.create"

    with patch(mock_target, return_value=None):
        response = auth_client.post(
            "/reports", json={"report": report, "media": [media["instance_metadata"]]}
        )

    assert response.status_code == 400


@patch(
    "routes.auth.CacheService.is_token_blocked",
    return_value=False,
    new_callable=AsyncMock,
)
def test_create_report_return_not_db_media(
    mock_is_token_blocked, auth_client, user, media
):

    report = {
        "user_id": user["id"],
        "location": {"longitude": 0.0, "latitude": 0.0},
        "type": "forest_fire",
        "intensity": "high",
    }

    mock_target = "api.routes.report.cruds.media_report_crud.create"

    with patch(mock_target, return_value=None):
        response = auth_client.post(
            "/reports", json={"report": report, "media": [media["instance_metadata"]]}
        )

    assert response.status_code == 400


@patch(
    "routes.auth.CacheService.is_token_blocked",
    return_value=False,
    new_callable=AsyncMock,
)
def test_read_report(mock_is_token_blocked, auth_client, report):

    report_id = report["id"]

    response = auth_client.get(f"/reports/{report_id}")

    assert response.status_code == 200


@patch(
    "routes.auth.CacheService.is_token_blocked",
    return_value=False,
    new_callable=AsyncMock,
)
def test_read_report_and_list_report_media(mock_is_token_blocked, auth_client, report):

    report_id = report["id"]

    response = auth_client.get(f"/reports/{report_id}/media")

    assert response.status_code == 200

    data = response.json()

    assert "total" in data
    assert "items" in data


##################################################################################################


# @patch("routes.auth.CacheService.is_token_blocked", return_value=False, new_callable=AsyncMock)
def test_update_report(mocked_admin_client, report):

    report_id = report["id"]

    response = mocked_admin_client.put(
        f"/reports/{report_id}",
        json={"type": "urban_fire"},
    )

    assert response.status_code == 200


def test_update_unknown_report(mocked_admin_client):

    report_id = "00000000-0000-0000-0000-000000000000"

    response = mocked_admin_client.put(
        f"/reports/{report_id}",
        json={"type": "urban_fire"},
    )

    assert response.status_code == 404


def test_delete_report(mocked_admin_client, report):

    report_id = report["id"]

    response = mocked_admin_client.delete(f"/reports/{report_id}")

    assert response.status_code == 204


def test_delete_unknown_report(mocked_admin_client):

    report_id = "00000000-0000-0000-0000-000000000000"

    response = mocked_admin_client.delete(f"/reports/{report_id}")

    assert response.status_code == 404


def test_list_reports(mocked_admin_client, report):

    response = mocked_admin_client.get("/reports")

    assert response.status_code == 200


###################################################################################################


##################################################################################################
