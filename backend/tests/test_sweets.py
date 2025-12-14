from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def get_token():
    response = client.post(
        "/api/auth/login",
        json={"username": "testuser", "password": "testpass"}
    )
    return response.json()["access_token"]

def test_create_sweet():
    token = get_token()
    response = client.post(
        "/api/sweets",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Rasgulla",
            "category": "Milk",
            "price": 20,
            "quantity": 50
        }
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Rasgulla"

def test_list_sweets():
    token = get_token()
    response = client.get(
        "/api/sweets",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_search_sweets_by_price():
    token = get_token()
    response = client.get(
        "/api/sweets/search?min_price=10&max_price=30",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
