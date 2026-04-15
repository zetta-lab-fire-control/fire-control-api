import pytest
import uuid


@pytest.fixture(scope="function")
def user_data():
    return {
        "firstname": "user",
        "lastname": "test",
        "email": f"user_{uuid.uuid4()}@example.com",
        "telephone": "123456789",
        "password": "securepassword",
    }


@pytest.fixture(scope="function")
def admin_data():
    return {
        "firstname": "admin",
        "lastname": "test",
        "email": f"admin_{uuid.uuid4()}@example.com",
        "telephone": "123456789",
        "password": "securepassword",
        "role": "admin",
    }


@pytest.fixture(scope="function")
def media_data():
    return {
        "bucket": "reports",
        "extension": "png",
        "type": "image",
        "size": 85,
        "description": "test image",
    }


@pytest.fixture(scope="function")
def report_data(user):
    return {
        "user_id": user["id"],
        "location": {"longitude": 0.0, "latitude": 0.0},
        "type": "forest_fire",
        "intensity": "high",
    }


@pytest.fixture(scope="function")
def occurrence_data():
    return {
        "location": {"longitude": 0.0, "latitude": 0.0},
        "type": "forest_fire",
        "intensity": "high",
        "status": "pending_confirmation",
    }
