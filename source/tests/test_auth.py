def test_login(client):
    response = client.post("/login")
    assert response.status_code == 200


def test_logout(client):
    response = client.post("/logout")
    assert response.status_code == 200


def test_password_reset(client):
    response = client.post("/password-reset")
    assert response.status_code == 200


def test_password_request(client):
    response = client.post("/password-request")
    assert response.status_code == 200
