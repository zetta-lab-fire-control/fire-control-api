from unittest.mock import patch


def test_create_user(user):

    assert "id" in user


def test_update_user(client, user):

    user_id = user["id"]

    response = client.put(
        f"/users/{user_id}",
        json={
            "firstname": "updated",
            "lastname": "user",
            "email": "updateduser@example.com",
            "telephone": "987654321",
            "password": "newsecurepassword",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == user_id


def test_delete_user(client, user):

    user_id = user["id"]

    response = client.delete(f"/users/{user_id}")

    assert response.status_code == 204


def test_get_user(client, user):

    user_id = user["id"]

    response = client.get(f"/users/{user_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == user_id


def test_list_users(client, user):

    response = client.get("/users")

    assert response.status_code == 200

    data = response.json()

    assert "total" in data and "items" in data


def test_create_user_returns_400(client):

    user = {
        "firstname": "user",
        "lastname": "test",
        "email": "test@example.com",
        "telephone": "123456789",
        "password": "securepassword",
    }

    mock_target = "api.routes.user.cruds.user_crud.create"

    with patch(mock_target, return_value=None):
        response = client.post("/users", json=user)

    assert response.status_code == 400

    assert response.json() == {"detail": "User could not be created"}


def test_get_user_returns_404(client):

    user_id = "00000000-0000-0000-0000-000000000000"

    response = client.get(f"/users/{user_id}")

    assert response.status_code == 404

    assert response.json() == {"detail": "User not found"}


def test_update_user_returns_404(client):

    user_id = "00000000-0000-0000-0000-000000000000"

    user_update = {
        "firstname": "updated",
        "lastname": "user",
        "email": "updateduser@example.com",
        "telephone": "987654321",
        "password": "newsecurepassword",
    }
    response = client.put(f"/users/{user_id}", json=user_update)

    assert response.status_code == 404

    assert response.json() == {"detail": "User not found"}


def test_delete_user_returns_404(client):

    user_id = "00000000-0000-0000-0000-000000000000"

    response = client.delete(f"/users/{user_id}")

    assert response.status_code == 404

    assert response.json() == {"detail": "User not found"}
