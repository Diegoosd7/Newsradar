"""
Pruebas funcionales E2E contra la API real (base de datos real, sin mocks).

Verifican que el sistema completo (router → service → BD) funciona correctamente.
Se ejecutan con: pytest tests/e2e/ -v
"""
import pytest
from uuid import uuid4


def unique_email():
    return f"e2e_{uuid4().hex[:8]}@test.com"


# ---------------------------------------------------------------------------
# Fixtures de autenticación compartidas por el módulo
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def registered_user(client):
    email = unique_email()
    password = "password123"
    response = client.post("/api/v1/auth/register", json={
        "email": email,
        "first_name": "E2E",
        "last_name": "Test",
        "organization": "TestOrg",
        "password": password,
        "role_ids": [],
    })
    assert response.status_code == 200, response.text
    data = response.json()
    return {"email": email, "password": password, "user_id": data["id"]}


@pytest.fixture(scope="module")
def auth_token(client, registered_user):
    response = client.post("/api/v1/auth/login", json={
        "email": registered_user["email"],
        "password": registered_user["password"],
    })
    assert response.status_code == 200, response.text
    return response.json()["access_token"]


@pytest.fixture(scope="module")
def auth_headers(auth_token):
    return {"Authorization": f"Bearer {auth_token}"}


# ---------------------------------------------------------------------------
# Sistema
# ---------------------------------------------------------------------------

class TestSystem:
    def test_health_check_returns_ok(self, client):
        response = client.get("/api/v1/system/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "timestamp" in data


# ---------------------------------------------------------------------------
# Autenticación
# ---------------------------------------------------------------------------

class TestAuth:
    def test_register_creates_user(self, client):
        response = client.post("/api/v1/auth/register", json={
            "email": unique_email(),
            "first_name": "New",
            "last_name": "User",
            "organization": "Org",
            "password": "pass123",
            "role_ids": [],
        })
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert data["is_verified"] is False

    def test_register_duplicate_email_fails(self, client, registered_user):
        response = client.post("/api/v1/auth/register", json={
            "email": registered_user["email"],
            "first_name": "Dup",
            "last_name": "User",
            "organization": "Org",
            "password": "pass123",
            "role_ids": [],
        })
        assert response.status_code == 409

    def test_register_missing_password_fails(self, client):
        response = client.post("/api/v1/auth/register", json={
            "email": unique_email(),
            "first_name": "No",
            "last_name": "Pass",
            "organization": "Org",
            "role_ids": [],
        })
        assert response.status_code == 422

    def test_login_valid_credentials_returns_token(self, client, registered_user):
        response = client.post("/api/v1/auth/login", json={
            "email": registered_user["email"],
            "password": registered_user["password"],
        })
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_wrong_password_fails(self, client, registered_user):
        response = client.post("/api/v1/auth/login", json={
            "email": registered_user["email"],
            "password": "wrongpassword",
        })
        assert response.status_code == 401

    def test_login_nonexistent_user_fails(self, client):
        response = client.post("/api/v1/auth/login", json={
            "email": "noexiste@test.com",
            "password": "pass123",
        })
        assert response.status_code == 401

    def test_protected_route_without_token_fails(self, client, registered_user):
        response = client.get(f"/api/v1/users/{registered_user['user_id']}/alerts")
        assert response.status_code == 401

    def test_protected_route_invalid_token_fails(self, client, registered_user):
        response = client.get(
            f"/api/v1/users/{registered_user['user_id']}/alerts",
            headers={"Authorization": "Bearer token-invalido-xyz"},
        )
        assert response.status_code == 401


# ---------------------------------------------------------------------------
# Alertas (CRUD completo)
# ---------------------------------------------------------------------------

class TestAlerts:
    _alert_id = None

    def test_list_alerts_initially_empty(self, client, registered_user, auth_headers):
        response = client.get(
            f"/api/v1/users/{registered_user['user_id']}/alerts",
            headers=auth_headers,
        )
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_create_alert(self, client, registered_user, auth_headers):
        response = client.post(
            f"/api/v1/users/{registered_user['user_id']}/alerts",
            json={
                "name": "Alerta E2E",
                "descriptors": ["tecnología", "IA"],
                "categories": [{"code": "04000000", "label": "Economía"}],
                "cron_expression": "0 * * * *",
            },
            headers=auth_headers,
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Alerta E2E"
        assert data["user_id"] == registered_user["user_id"]
        TestAlerts._alert_id = data["id"]

    def test_list_alerts_after_create(self, client, registered_user, auth_headers):
        response = client.get(
            f"/api/v1/users/{registered_user['user_id']}/alerts",
            headers=auth_headers,
        )
        assert response.status_code == 200
        ids = [a["id"] for a in response.json()]
        assert TestAlerts._alert_id in ids

    def test_get_alert_by_id(self, client, registered_user, auth_headers):
        response = client.get(
            f"/api/v1/users/{registered_user['user_id']}/alerts/{TestAlerts._alert_id}",
            headers=auth_headers,
        )
        assert response.status_code == 200
        assert response.json()["id"] == TestAlerts._alert_id

    def test_update_alert_name(self, client, registered_user, auth_headers):
        response = client.put(
            f"/api/v1/users/{registered_user['user_id']}/alerts/{TestAlerts._alert_id}",
            json={"name": "Alerta E2E Actualizada"},
            headers=auth_headers,
        )
        assert response.status_code == 200
        assert response.json()["name"] == "Alerta E2E Actualizada"

    def test_create_alert_missing_name_fails(self, client, registered_user, auth_headers):
        response = client.post(
            f"/api/v1/users/{registered_user['user_id']}/alerts",
            json={
                "descriptors": ["test"],
                "categories": [{"code": "X", "label": "X"}],
                "cron_expression": "0 * * * *",
            },
            headers=auth_headers,
        )
        assert response.status_code == 422

    def test_get_nonexistent_alert_fails(self, client, registered_user, auth_headers):
        response = client.get(
            f"/api/v1/users/{registered_user['user_id']}/alerts/99999",
            headers=auth_headers,
        )
        assert response.status_code == 404

    def test_delete_alert(self, client, registered_user, auth_headers):
        response = client.delete(
            f"/api/v1/users/{registered_user['user_id']}/alerts/{TestAlerts._alert_id}",
            headers=auth_headers,
        )
        assert response.status_code == 204

    def test_get_deleted_alert_fails(self, client, registered_user, auth_headers):
        response = client.get(
            f"/api/v1/users/{registered_user['user_id']}/alerts/{TestAlerts._alert_id}",
            headers=auth_headers,
        )
        assert response.status_code == 404


# ---------------------------------------------------------------------------
# Notificaciones
# ---------------------------------------------------------------------------

class TestNotifications:
    def test_list_notifications_returns_list(self, client, registered_user, auth_headers):
        response = client.get(
            f"/api/v1/users/{registered_user['user_id']}/notifications",
            headers=auth_headers,
        )
        assert response.status_code == 200
        assert isinstance(response.json(), list)


# ---------------------------------------------------------------------------
# Categorías (CRUD)
# ---------------------------------------------------------------------------

class TestCategories:
    _category_id = None

    def test_create_category(self, client, auth_headers):
        response = client.post(
            "/api/v1/categories",
            json={"name": "Categoría E2E", "source": "IPTC"},
            headers=auth_headers,
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Categoría E2E"
        TestCategories._category_id = data["id"]

    def test_list_categories_contains_created(self, client, auth_headers):
        response = client.get("/api/v1/categories", headers=auth_headers)
        assert response.status_code == 200
        ids = [c["id"] for c in response.json()]
        assert TestCategories._category_id in ids

    def test_get_category_by_id(self, client, auth_headers):
        response = client.get(
            f"/api/v1/categories/{TestCategories._category_id}",
            headers=auth_headers,
        )
        assert response.status_code == 200
        assert response.json()["id"] == TestCategories._category_id

    def test_delete_category(self, client, auth_headers):
        response = client.delete(
            f"/api/v1/categories/{TestCategories._category_id}",
            headers=auth_headers,
        )
        assert response.status_code == 204

    def test_get_deleted_category_fails(self, client, auth_headers):
        response = client.get(
            f"/api/v1/categories/{TestCategories._category_id}",
            headers=auth_headers,
        )
        assert response.status_code == 404


# ---------------------------------------------------------------------------
# Fuentes de información (CRUD)
# ---------------------------------------------------------------------------

class TestInformationSources:
    _source_id = None

    def test_create_information_source(self, client, auth_headers):
        response = client.post(
            "/api/v1/information-sources",
            json={"name": "Fuente E2E", "url": "https://e2e-test.example.com"},
            headers=auth_headers,
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Fuente E2E"
        TestInformationSources._source_id = data["id"]

    def test_list_information_sources(self, client, auth_headers):
        response = client.get("/api/v1/information-sources", headers=auth_headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_delete_information_source(self, client, auth_headers):
        response = client.delete(
            f"/api/v1/information-sources/{TestInformationSources._source_id}",
            headers=auth_headers,
        )
        assert response.status_code == 204
