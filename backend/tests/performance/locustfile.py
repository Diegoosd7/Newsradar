"""
Pruebas de rendimiento con Locust para la API de NewsRadar.

Uso:
    # Arrancar el backend primero:
    cd backend && uvicorn app.main:app --host 0.0.0.0 --port 8000

    # Ejecutar en modo headless (sin UI):
    locust -f tests/performance/locustfile.py \
        --host http://localhost:8000 \
        --users 20 --spawn-rate 2 --run-time 60s --headless

    # Ejecutar con UI web (abrir http://localhost:8089):
    locust -f tests/performance/locustfile.py --host http://localhost:8000
"""

import uuid
from locust import HttpUser, task, between


class NewsRadarUser(HttpUser):
    """
    Simula un usuario típico de NewsRadar:
    se registra, inicia sesión y luego alterna
    entre consultar alertas, notificaciones y categorías.
    """

    wait_time = between(1, 3)

    def on_start(self):
        """Registro + login antes de iniciar las tareas de carga."""
        self.user_id = None
        self.token = None
        self.headers = {}
        self._alert_ids: list[int] = []

        email = f"locust_{uuid.uuid4().hex[:10]}@loadtest.com"
        password = "locust123"

        reg = self.client.post(
            "/api/v1/auth/register",
            json={
                "email": email,
                "first_name": "Load",
                "last_name": "Test",
                "organization": "Locust",
                "password": password,
                "role_ids": [],
            },
            name="/api/v1/auth/register [setup]",
        )
        if reg.status_code != 200:
            return

        self.user_id = reg.json().get("id")

        login = self.client.post(
            "/api/v1/auth/login",
            json={"email": email, "password": password},
            name="/api/v1/auth/login [setup]",
        )
        if login.status_code != 200:
            return

        self.token = login.json().get("access_token")
        self.headers = {"Authorization": f"Bearer {self.token}"}

    # ------------------------------------------------------------------
    # Tareas (peso relativo = frecuencia aproximada de uso real)
    # ------------------------------------------------------------------

    @task(10)
    def health_check(self):
        """Endpoint público de salud — baseline de latencia."""
        self.client.get("/api/v1/health")

    @task(6)
    def list_alerts(self):
        """Listado de alertas del usuario — operación más frecuente."""
        if not self.user_id:
            return
        self.client.get(
            f"/api/v1/users/{self.user_id}/alerts",
            headers=self.headers,
            name="/api/v1/users/[id]/alerts GET",
        )

    @task(4)
    def list_notifications(self):
        """Listado de notificaciones — lectura habitual."""
        if not self.user_id:
            return
        self.client.get(
            f"/api/v1/users/{self.user_id}/notifications",
            headers=self.headers,
            name="/api/v1/users/[id]/notifications GET",
        )

    @task(3)
    def list_categories(self):
        """Catálogo de categorías IPTC — consulta de referencia."""
        if not self.token:
            return
        self.client.get("/api/v1/categories", headers=self.headers)

    @task(2)
    def list_information_sources(self):
        """Listado de fuentes de información."""
        if not self.token:
            return
        self.client.get("/api/v1/information-sources", headers=self.headers)

    @task(2)
    def create_alert(self):
        """Creación de alerta — operación de escritura moderada."""
        if not self.user_id:
            return
        resp = self.client.post(
            f"/api/v1/users/{self.user_id}/alerts",
            json={
                "name": f"Alerta Locust {uuid.uuid4().hex[:4]}",
                "descriptors": ["tecnología", "economía"],
                "categories": [{"code": "04000000", "label": "Economía"}],
                "cron_expression": "0 * * * *",
            },
            headers=self.headers,
            name="/api/v1/users/[id]/alerts POST",
        )
        if resp.status_code == 201:
            self._alert_ids.append(resp.json()["id"])

    @task(1)
    def delete_alert(self):
        """Elimina una alerta creada durante la sesión de carga."""
        if not self.user_id or not self._alert_ids:
            return
        alert_id = self._alert_ids.pop(0)
        self.client.delete(
            f"/api/v1/users/{self.user_id}/alerts/{alert_id}",
            headers=self.headers,
            name="/api/v1/users/[id]/alerts/[id] DELETE",
        )
