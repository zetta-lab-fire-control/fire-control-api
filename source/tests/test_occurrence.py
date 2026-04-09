from datetime import datetime, timedelta
from unittest.mock import patch


def test_create_occurrence(client, occurrence):

    assert "id" in occurrence


def test_update_occurrence(client, occurrence):

    occurrence_id = occurrence["id"]

    response = client.put(
        f"/occurrences/{occurrence_id}",
        json={
            "status": "resolved",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == occurrence_id


def test_delete_occurrence(client, occurrence):

    occurrence_id = occurrence["id"]

    response = client.delete(f"/occurrences/{occurrence_id}")

    assert response.status_code == 204


def test_read_occurrence(client, occurrence):

    occurrence_id = occurrence["id"]

    response = client.get(f"/occurrences/{occurrence_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == occurrence_id


def test_list_occurrences(client, occurrence):

    response = client.get("/occurrences")

    assert response.status_code == 200

    data = response.json()

    assert "items" in data
    assert "total" in data


def test_create_occurrence_return_not_db_occurrence(client):

    occurrence = {
        "location": {"longitude": 0.0, "latitude": 0.0},
        "type": "forest_fire",
        "intensity": "high",
        "status": "pending_confirmation",
    }

    mock_create = "api.routes.occurrence.cruds.occurrence_crud.create"

    with patch(mock_create, return_value=None):
        response = client.post(
            "/occurrences",
            json=occurrence,
        )

    assert response.status_code == 400


def test_update_occurrence_return_not_db_occurrence(client, occurrence):

    occurrence_id = "00000000-0000-0000-0000-000000000000"

    response = client.put(
        f"/occurrences/{occurrence_id}",
        json={
            "status": "resolved",
        },
    )

    assert response.status_code == 404


def test_delete_occurrence_return_not_db_occurrence(client):

    occurrence_id = "00000000-0000-0000-0000-000000000000"

    response = client.delete(f"/occurrences/{occurrence_id}")

    assert response.status_code == 404


def test_read_occurrence_return_not_db_occurrence(client):

    occurrence_id = "00000000-0000-0000-0000-000000000000"

    response = client.get(f"/occurrences/{occurrence_id}")

    assert response.status_code == 404


def test_occurrence_operational_indicators(client, occurrence):

    city = "Lavras,MG"
    target_date = datetime.now()

    response = client.get(
        "/occurrences/indicators/operational",
        params={"city": city, "target_date": target_date.isoformat()},
    )

    assert response.status_code == 200


def test_occurrence_public_indicators(client, occurrence):

    response = client.get("/occurrences/indicators/public")

    assert response.status_code == 200


def test_occurrence_history(client, occurrence):

    start_date = datetime.now() - timedelta(days=30)
    end_date = datetime.now()

    response = client.get(
        "/occurrences/indicators/history",
        params={"start_date": start_date.isoformat(), "end_date": end_date.isoformat()},
    )

    assert response.status_code == 200
