def test_api_health(client):
    response = client.get("/health")
    assert response.status_code == 200


def test_api_home(client):
    response = client.get("/")
    assert response.status_code == 200
