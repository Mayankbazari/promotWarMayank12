import pytest
from agents.classifier import classify_emergency
from main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_location_extraction_in_response():
    """Test that the location extraction logic works and returns a Google Maps URL."""
    payload = {"text": "Accident at ORR Bangalore near the bridge"}
    response = client.post("/analyze", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert "google_maps_url" in data
    assert "google.com/maps" in data.get("google_maps_url")
    assert "ORR+Bangalore" in data.get("google_maps_url")

def test_health_check_healthiness():
    """Verify health check endpoint returns 200."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
