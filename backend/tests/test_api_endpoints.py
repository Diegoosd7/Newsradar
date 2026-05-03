import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient

from app.main import app
from app.features.auth.router import get_auth_service
from app.features.alerts.router import get_alerts_service
from app.core.security import get_current_user


class FakeAuthService:
    def login(self, payload):
        return {
            "access_token": "fake-token-123",
            "token_type": "bearer",
            "user": {
                "id": 1,
                "email": payload.email if hasattr(payload, 'email') else "test@example.com",
                "first_name": "Test",
                "last_name": "User",
                "organization": "UC3M",
                "is_verified": True
            }
        }

    def register(self, payload):
        return {
            "id": 1,
            "email": payload.email,
            "first_name": payload.first_name,
            "last_name": payload.last_name,
            "organization": payload.organization,
            "role_ids": payload.role_ids,
        }


class FakeAlertsService:
    def list_user_alerts(self, user_id):
        return [
            {
                "id": 1,
                "user_id": user_id,
                "name": "AI News",
                "descriptors": ["ai", "machine learning"],
                "categories": [{"code": "tech", "label": "Technology"}],
                "cron_expression": "0 * * * *",
            }
        ]

    def create_user_alert(self, user_id, payload):
        return {
            "id": 2,
            "user_id": user_id,
            "name": payload.name,
            "descriptors": payload.descriptors,
            "categories": [category.model_dump() for category in payload.categories],
            "cron_expression": payload.cron_expression,
        }

    def get_user_alert(self, user_id, alert_id):
        return {
            "id": alert_id,
            "user_id": user_id,
            "name": "Cybersecurity Alert",
            "descriptors": ["cyber", "security"],
            "categories": [{"code": "security", "label": "Security"}],
            "cron_expression": "*/15 * * * *",
        }

    def update_user_alert(self, user_id, alert_id, payload):
        return {
            "id": alert_id,
            "user_id": user_id,
            "name": payload.name if payload.name is not None else "Updated Alert",
            "descriptors": payload.descriptors if payload.descriptors is not None else ["updated"],
            "categories": (
                [category.model_dump() for category in payload.categories]
                if payload.categories is not None
                else [{"code": "updated", "label": "Updated"}]
            ),
            "cron_expression": (
                payload.cron_expression
                if payload.cron_expression is not None
                else "0 0 * * *"
            ),
        }

    def delete_user_alert(self, user_id, alert_id):
        return None


def fake_current_user():
    return {
        "id": 999,
        "email": "tester@example.com",
        "first_name": "Test",
        "last_name": "User",
        "organization": "UC3M",
        "role_ids": [1],
        "password": "secret123",
    }


@pytest.fixture(autouse=True, scope="module")
def _setup_overrides():
    app.dependency_overrides[get_auth_service] = lambda: FakeAuthService()
    app.dependency_overrides[get_alerts_service] = lambda: FakeAlertsService()
    app.dependency_overrides[get_current_user] = fake_current_user
    yield
    app.dependency_overrides.pop(get_auth_service, None)
    app.dependency_overrides.pop(get_alerts_service, None)
    app.dependency_overrides.pop(get_current_user, None)


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/api/v1/system/health")
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "ok"
    assert "timestamp" in data


def test_register_user():
    payload = {
        "email": "newuser@example.com",
        "first_name": "Pablo",
        "last_name": "Garcia",
        "organization": "UC3M",
        "role_ids": [1],
        "password": "secret123",
    }

    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == 1
    assert data["email"] == payload["email"]
    assert data["first_name"] == payload["first_name"]
    assert data["last_name"] == payload["last_name"]
    assert data["organization"] == payload["organization"]
    assert data["role_ids"] == payload["role_ids"]


def test_register_user_missing_required_field():
    payload = {
        "email": "newuser@example.com",
        "first_name": "Pablo",
        "last_name": "Garcia",
        "organization": "UC3M",
        "role_ids": [1],
        # falta password
    }

    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 422


def test_login_user():
    payload = {
        "email": "newuser@example.com",
        "password": "secret123",
    }

    response = client.post("/api/v1/auth/login", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert data["access_token"] == "fake-token-123"
    assert data["token_type"] == "bearer"
    assert "user" in data


def test_login_user_missing_password():
    payload = {
        "email": "newuser@example.com",
    }

    response = client.post("/api/v1/auth/login", json=payload)
    assert response.status_code == 422


def test_list_user_alerts():
    response = client.get("/api/v1/users/1/alerts")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["user_id"] == 1
    assert data[0]["name"] == "AI News"


def test_list_user_alerts_invalid_user_id():
    response = client.get("/api/v1/users/invalid/alerts")
    assert response.status_code == 422


def test_create_user_alert():
    payload = {
        "name": "Tech Alert",
        "descriptors": ["ai", "robotics"],
        "categories": [{"code": "tech", "label": "Technology"}],
        "cron_expression": "0 * * * *",
    }

    response = client.post("/api/v1/users/1/alerts", json=payload)
    assert response.status_code == 201

    data = response.json()
    assert data["id"] == 2
    assert data["user_id"] == 1
    assert data["name"] == payload["name"]
    assert data["descriptors"] == payload["descriptors"]
    assert data["categories"] == payload["categories"]
    assert data["cron_expression"] == payload["cron_expression"]


def test_create_user_alert_missing_name():
    payload = {
        "descriptors": ["ai", "robotics"],
        "categories": [{"code": "tech", "label": "Technology"}],
        "cron_expression": "0 * * * *",
    }

    response = client.post("/api/v1/users/1/alerts", json=payload)
    assert response.status_code == 422


def test_create_user_alert_missing_descriptors():
    payload = {
        "name": "Tech Alert",
        "categories": [{"code": "tech", "label": "Technology"}],
        "cron_expression": "0 * * * *",
    }

    response = client.post("/api/v1/users/1/alerts", json=payload)
    assert response.status_code == 422


def test_create_user_alert_invalid_user_id():
    payload = {
        "name": "Tech Alert",
        "descriptors": ["ai", "robotics"],
        "categories": [{"code": "tech", "label": "Technology"}],
        "cron_expression": "0 * * * *",
    }

    response = client.post("/api/v1/users/invalid/alerts", json=payload)
    assert response.status_code == 422


def test_get_user_alert():
    response = client.get("/api/v1/users/1/alerts/7")
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == 7
    assert data["user_id"] == 1
    assert data["name"] == "Cybersecurity Alert"


def test_get_user_alert_invalid_alert_id():
    response = client.get("/api/v1/users/1/alerts/invalid")
    assert response.status_code == 422


def test_update_user_alert():
    payload = {
        "name": "Updated Tech Alert",
        "descriptors": ["cloud", "devops"],
        "categories": [{"code": "it", "label": "IT"}],
        "cron_expression": "*/30 * * * *",
    }

    response = client.put("/api/v1/users/1/alerts/7", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == 7
    assert data["user_id"] == 1
    assert data["name"] == payload["name"]
    assert data["descriptors"] == payload["descriptors"]
    assert data["categories"] == payload["categories"]
    assert data["cron_expression"] == payload["cron_expression"]


def test_update_user_alert_partial_payload():
    payload = {
        "name": "Partially Updated Alert",
    }

    response = client.put("/api/v1/users/1/alerts/7", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == 7
    assert data["user_id"] == 1
    assert data["name"] == "Partially Updated Alert"


def test_update_user_alert_invalid_alert_id():
    payload = {
        "name": "Updated Tech Alert",
    }

    response = client.put("/api/v1/users/1/alerts/invalid", json=payload)
    assert response.status_code == 422


def test_delete_user_alert():
    response = client.delete("/api/v1/users/1/alerts/7")
    assert response.status_code == 204
    assert response.text == ""


def test_delete_user_alert_invalid_alert_id():
    response = client.delete("/api/v1/users/1/alerts/invalid")
    assert response.status_code == 422