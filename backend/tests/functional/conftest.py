import os
import sys

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.main import app
from app.features.auth.router import get_auth_service
from app.features.alerts.router import get_alerts_service
from app.core.security import get_current_user


class FakeAuthService:
    def login(self, payload):
        return {
            "access_token": "fake-token-123",
            "token_type": "bearer",
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


@pytest.fixture
def client():
    app.dependency_overrides[get_auth_service] = lambda: FakeAuthService()
    app.dependency_overrides[get_alerts_service] = lambda: FakeAlertsService()
    app.dependency_overrides[get_current_user] = fake_current_user

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()