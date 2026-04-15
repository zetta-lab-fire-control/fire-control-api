import pytest


@pytest.fixture(scope="function")
def occurrence(mocked_admin_client, occurrence_data):

    response = mocked_admin_client.post(
        "/occurrences",
        json=occurrence_data,
    )
    assert response.status_code == 201

    return response.json()
