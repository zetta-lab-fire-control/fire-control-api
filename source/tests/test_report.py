from unittest.mock import patch


def test_create_report(report):

    assert "id" in report


def test_update_report(client, report):

    report_id = report["id"]

    response = client.put(
        f"/reports/{report_id}",
        json={"type": "urban_fire"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == report_id


def test_delete_report(client, report):

    report_id = report["id"]

    response = client.delete(f"/reports/{report_id}")

    assert response.status_code == 204


def test_read_report(client, report):

    report_id = report["id"]

    response = client.get(f"/reports/{report_id}")

    assert response.status_code == 200


def test_list_reports(client, report):

    response = client.get("/reports")

    assert response.status_code == 200

    data = response.json()

    assert "total" in data
    assert "items" in data


def test_list_report_media(client, report):

    report_id = report["id"]

    response = client.get(f"/reports/{report_id}/media")

    assert response.status_code == 200

    data = response.json()

    assert "total" in data
    assert "items" in data


def test_create_report_return_not_db_occurrence(client, user, media):

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
            response = client.post(
                "/reports",
                json={"report": report, "media": [media["instance_metadata"]]},
            )

    assert response.status_code == 400


def test_create_report_return_not_db_report_error_400(client, user, media):

    report = {
        "user_id": user["id"],
        "location": {"longitude": 0.0, "latitude": 0.0},
        "type": "forest_fire",
        "intensity": "high",
    }

    mock_target = "api.routes.report.cruds.report_crud.create"

    with patch(mock_target, return_value=None):
        response = client.post(
            "/reports", json={"report": report, "media": [media["instance_metadata"]]}
        )

    assert response.status_code == 400


def test_create_report_return_not_db_media_error_400(client, user, media):

    report = {
        "user_id": user["id"],
        "location": {"longitude": 0.0, "latitude": 0.0},
        "type": "forest_fire",
        "intensity": "high",
    }

    mock_target = "api.routes.report.cruds.media_report_crud.create"

    with patch(mock_target, return_value=None):
        response = client.post(
            "/reports", json={"report": report, "media": [media["instance_metadata"]]}
        )

    assert response.status_code == 400


def test_update_report_return_not_db_report_error_404(client):

    report_id = "00000000-0000-0000-0000-000000000000"

    response = client.put(
        f"/reports/{report_id}",
        json={"type": "urban_fire", "intensity": "medium"},
    )

    assert response.status_code == 404


def test_delete_report_return_not_db_report(client):

    report_id = "00000000-0000-0000-0000-000000000000"

    response = client.delete(f"/reports/{report_id}")

    assert response.status_code == 404


def test_read_report_return_not_db_report_error_404(client):

    report_id = "00000000-0000-0000-0000-000000000000"

    response = client.get(f"/reports/{report_id}")

    assert response.status_code == 404
