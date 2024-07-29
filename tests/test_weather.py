from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_weather():
    response = client.get("/weather?city=curitiba")
    assert response.status_code == 200
    assert "message" in response.json()