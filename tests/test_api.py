"""Automated tests for the AI Security Data Platform API."""

import pytest
from fastapi.testclient import TestClient

from app import database
from app.main import app


@pytest.fixture
def client(tmp_path, monkeypatch):
    """Create an API client using a temporary test database."""
    test_database = tmp_path / "test_security_events.db"
    monkeypatch.setattr(database, "DATABASE_PATH", test_database)

    with TestClient(app) as test_client:
        yield test_client


def test_health_check(client):
    """The health endpoint should report a healthy platform."""
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_create_and_list_event(client):
    """A valid event should be stored and returned."""
    event = {
        "device_id": "camera-test-01",
        "event_type": "motion_detected",
        "severity": "medium",
        "description": "Automated test motion event",
        "confidence": 0.95,
    }

    create_response = client.post("/events", json=event)

    assert create_response.status_code == 201
    created_event = create_response.json()
    assert created_event["id"] == 1
    assert created_event["device_id"] == "camera-test-01"

    list_response = client.get("/events")

    assert list_response.status_code == 200
    events = list_response.json()
    assert len(events) == 1
    assert events[0]["event_type"] == "motion_detected"


def test_rejects_invalid_confidence(client):
    """Confidence values above 1.0 should be rejected."""
    event = {
        "device_id": "camera-test-02",
        "event_type": "person_detected",
        "severity": "high",
        "description": "Invalid confidence test",
        "confidence": 1.5,
    }

    response = client.post("/events", json=event)

    assert response.status_code == 422