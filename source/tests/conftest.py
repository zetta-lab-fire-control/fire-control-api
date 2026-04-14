import os
import uuid

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api.app import app
from api.clients.postgres import PostgresClient
from api.core.security.service import TokenService

URL: str | None = os.getenv("DATABASE_URL")


@pytest.fixture(scope="session")
def engine():

    return create_engine(URL, connect_args={"client_encoding": "utf8"})


@pytest.fixture(scope="session", autouse=True)
def setup_database(engine):

    Base = PostgresClient.Base

    Base.metadata.create_all(bind=engine)

    yield

    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session(engine):

    connection = engine.connect()

    transaction = connection.begin()

    local = sessionmaker(
        bind=connection,
        autocommit=False,
        autoflush=False,
        join_transaction_mode="create_savepoint",
    )

    session = local()

    yield session

    session.close()

    transaction.rollback()

    connection.close()


@pytest.fixture(scope="function")
def client(db_session):

    def _get_db_session_():

        yield db_session

    app.dependency_overrides[PostgresClient.db] = _get_db_session_

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()


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
def user(client, user_data):

    response = client.post(
        "/users",
        json=user_data,
        headers={},
    )

    data = response.json()

    if "id" not in data:
        pytest.fail(f"Failed to create test user: {data}")

    return data


@pytest.fixture(scope="function")
def media(client, user):

    media = {
        "bucket": "reports",
        "extension": "png",
        "type": "image",
        "size": 85,
        "description": "test image",
    }

    response = client.post(
        "/media",
        json=media,
    )

    return response.json()


@pytest.fixture(scope="function")
def report(client, user, media):

    report = {
        "user_id": user["id"],
        "location": {"longitude": 0.0, "latitude": 0.0},
        "type": "forest_fire",
        "intensity": "high",
    }

    media_instance_list = [media["instance_metadata"]]

    response = client.post(
        "/reports",
        json={"report": report, "media": media_instance_list},
    )

    return response.json()


@pytest.fixture(scope="function")
def occurrence(client):
    occurrence = {
        "location": {"longitude": 0.0, "latitude": 0.0},
        "type": "forest_fire",
        "intensity": "high",
        "status": "pending_confirmation",
    }

    response = client.post(
        "/occurrences",
        json=occurrence,
    )

    return response.json()


@pytest.fixture(scope="function")
def user_acess_token(user):
    access_token = TokenService().create_access_token(data={"sub": user["id"]})
    return access_token


@pytest.fixture(scope="function")
def user_reset_token(user):
    reset_token = TokenService().create_reset_token(data={"sub": user["id"]})
    return reset_token


@pytest.fixture(scope="function")
def user_refresh_token(user):
    refresh_token = TokenService().create_refresh_token(data={"sub": user["id"]})
    return refresh_token


@pytest.fixture(scope="function")
def auth_client(client, user_acess_token):
    client.headers = {**client.headers, "Authorization": f"Bearer {user_acess_token}"}
    return client


@pytest.fixture(scope="function")
def user_credentials(user_data):
    return {"username": user_data["email"], "password": user_data["password"]}
