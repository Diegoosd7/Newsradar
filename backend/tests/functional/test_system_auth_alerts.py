from fastapi import HTTPException

from app.main import app
from app.features.auth.router import get_auth_service
from app.features.alerts.router import get_alerts_service

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

class FailingAuthService:
    def login(self, payload):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    def register(self, payload):
        raise HTTPException(status_code=409, detail="El email ya está registrado")


class NotFoundAlertsService:
    def list_user_alerts(self, user_id):
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    def create_user_alert(self, user_id, payload):
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    def get_user_alert(self, user_id, alert_id):
        raise HTTPException(status_code=404, detail="Alerta no encontrada para el usuario")

    def update_user_alert(self, user_id, alert_id, payload):
        raise HTTPException(status_code=404, detail="Alerta no encontrada para el usuario")

    def delete_user_alert(self, user_id, alert_id):
        raise HTTPException(status_code=404, detail="Alerta no encontrada para el usuario")


class LimitAlertsService:
    def list_user_alerts(self, user_id):
        return []

    def create_user_alert(self, user_id, payload):
        raise HTTPException(
            status_code=400,
            detail="Límite máximo de 20 alertas alcanzado para este usuario.",
        )

    def get_user_alert(self, user_id, alert_id):
        raise HTTPException(status_code=404, detail="Alerta no encontrada para el usuario")

    def update_user_alert(self, user_id, alert_id, payload):
        raise HTTPException(status_code=404, detail="Alerta no encontrada para el usuario")

    def delete_user_alert(self, user_id, alert_id):
        raise HTTPException(status_code=404, detail="Alerta no encontrada para el usuario")


def test_health_endpoint(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "ok"
    assert "timestamp" in data


def test_register_user(client):
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


def test_register_user_missing_required_field(client):
    payload = {
        "email": "newuser@example.com",
        "first_name": "Pablo",
        "last_name": "Garcia",
        "organization": "UC3M",
        "role_ids": [1],
    }

    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 422


def test_register_user_duplicate_email(client):
    app.dependency_overrides[get_auth_service] = lambda: FailingAuthService()

    payload = {
        "email": "existing@example.com",
        "first_name": "Pablo",
        "last_name": "Garcia",
        "organization": "UC3M",
        "role_ids": [1],
        "password": "secret123",
    }

    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 409
    assert response.json()["detail"] == "El email ya está registrado"


def test_login_user(client):
    app.dependency_overrides[get_auth_service] = lambda: FakeAuthService()
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


def test_login_user_missing_password(client):
    payload = {
        "email": "newuser@example.com",
    }

    response = client.post("/api/v1/auth/login", json=payload)
    assert response.status_code == 422


def test_login_user_invalid_credentials(client):
    app.dependency_overrides[get_auth_service] = lambda: FailingAuthService()

    payload = {
        "email": "wrong@example.com",
        "password": "bad-password",
    }

    response = client.post("/api/v1/auth/login", json=payload)
    assert response.status_code == 401
    assert response.json()["detail"] == "Credenciales inválidas"


def test_list_user_alerts(client):
    response = client.get("/api/v1/users/1/alerts")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["user_id"] == 1
    assert data[0]["name"] == "AI News"


def test_list_user_alerts_invalid_user_id(client):
    response = client.get("/api/v1/users/invalid/alerts")
    assert response.status_code == 422


def test_list_user_alerts_user_not_found(client):
    app.dependency_overrides[get_alerts_service] = lambda: NotFoundAlertsService()

    response = client.get("/api/v1/users/99999/alerts")
    assert response.status_code == 404
    assert response.json()["detail"] == "Usuario no encontrado"


def test_create_user_alert(client):
    payload = {
        "name": "Tech Alert",
        "descriptors": ["ai", "robotics", "machine learning"],
        "categories": [{"code": "13000000", "label": "Ciencia y tecnología"}],
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


def test_create_user_alert_missing_name(client):
    payload = {
        "descriptors": ["ai", "robotics"],
        "categories": [{"code": "tech", "label": "Technology"}],
        "cron_expression": "0 * * * *",
    }

    response = client.post("/api/v1/users/1/alerts", json=payload)
    assert response.status_code == 422


def test_create_user_alert_invalid_user_id(client):
    payload = {
        "name": "Tech Alert",
        "descriptors": ["ai", "robotics"],
        "categories": [{"code": "tech", "label": "Technology"}],
        "cron_expression": "0 * * * *",
    }

    response = client.post("/api/v1/users/invalid/alerts", json=payload)
    assert response.status_code == 422


def test_create_user_alert_limit_reached(client):
    app.dependency_overrides[get_alerts_service] = lambda: LimitAlertsService()

    payload = {
        "name": "Tech Alert",
        "descriptors": ["ai", "robotics", "machine learning"],
        "categories": [{"code": "13000000", "label": "Ciencia y tecnología"}],
        "cron_expression": "0 * * * *",
    }

    response = client.post("/api/v1/users/1/alerts", json=payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "Límite máximo de 20 alertas alcanzado para este usuario."


def test_get_user_alert(client):
    response = client.get("/api/v1/users/1/alerts/7")
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == 7
    assert data["user_id"] == 1
    assert data["name"] == "Cybersecurity Alert"


def test_get_user_alert_invalid_alert_id(client):
    response = client.get("/api/v1/users/1/alerts/invalid")
    assert response.status_code == 422


def test_get_user_alert_not_found(client):
    app.dependency_overrides[get_alerts_service] = lambda: NotFoundAlertsService()

    response = client.get("/api/v1/users/1/alerts/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Alerta no encontrada para el usuario"


def test_update_user_alert(client):
    payload = {
        "name": "Updated Tech Alert",
        "descriptors": ["cloud", "devops", "infra"],
        "categories": [{"code": "13000000", "label": "Ciencia y tecnología"}],
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


def test_update_user_alert_partial_payload(client):
    payload = {
        "name": "Partially Updated Alert",
    }

    response = client.put("/api/v1/users/1/alerts/7", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == 7
    assert data["user_id"] == 1
    assert data["name"] == "Partially Updated Alert"


def test_update_user_alert_invalid_alert_id(client):
    payload = {
        "name": "Updated Tech Alert",
    }

    response = client.put("/api/v1/users/1/alerts/invalid", json=payload)
    assert response.status_code == 422


def test_update_user_alert_not_found(client):
    app.dependency_overrides[get_alerts_service] = lambda: NotFoundAlertsService()

    payload = {
        "name": "Updated Tech Alert",
    }

    response = client.put("/api/v1/users/1/alerts/99999", json=payload)
    assert response.status_code == 404
    assert response.json()["detail"] == "Alerta no encontrada para el usuario"


def test_delete_user_alert(client):
    response = client.delete("/api/v1/users/1/alerts/7")
    assert response.status_code == 204
    assert response.text == ""


def test_delete_user_alert_invalid_alert_id(client):
    response = client.delete("/api/v1/users/1/alerts/invalid")
    assert response.status_code == 422


def test_delete_user_alert_not_found(client):
    app.dependency_overrides[get_alerts_service] = lambda: NotFoundAlertsService()

    response = client.delete("/api/v1/users/1/alerts/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Alerta no encontrada para el usuario"