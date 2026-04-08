"""
PLANTILLA PARA CUBRIR EL PUNTO 1:
users
roles
information_sources
rss_channels
notifications
stats
categories

IMPORTANTE:
- Cambia las rutas si en vuestro proyecto no coinciden.
- Cambia los payloads según vuestros schemas reales.
- Si algún endpoint requiere auth, el fixture `client` ya entra autenticado.
"""

import pytest


# AJUSTA SOLO ESTA CONFIG
MODULE_CASES = [
    # USERS
    {
        "name": "list_users",
        "method": "get",
        "path": "/api/v1/users",
        "json": None,
        "expected_statuses": {200},
    },
    {
        "name": "get_user_by_id",
        "method": "get",
        "path": "/api/v1/users/1",
        "json": None,
        "expected_statuses": {200, 404},
    },

    # ROLES
    {
        "name": "list_roles",
        "method": "get",
        "path": "/api/v1/roles",
        "json": None,
        "expected_statuses": {200},
    },

    # INFORMATION SOURCES
    {
        "name": "list_information_sources",
        "method": "get",
        "path": "/api/v1/information-sources",
        "json": None,
        "expected_statuses": {200},
    },

    # RSS CHANNELS
    {
        "name": "list_rss_channels",
        "method": "get",
        "path": "/api/v1/rss-channels",
        "json": None,
        "expected_statuses": {200},
    },

    # NOTIFICATIONS
    {
        "name": "list_notifications",
        "method": "get",
        "path": "/api/v1/users/1/notifications",
        "json": None,
        "expected_statuses": {200},
    },

    # STATS
    {
        "name": "get_stats",
        "method": "get",
        "path": "/api/v1/stats",
        "json": None,
        "expected_statuses": {200},
    },

    # CATEGORIES
    {
        "name": "list_categories",
        "method": "get",
        "path": "/api/v1/categories",
        "json": None,
        "expected_statuses": {200},
    },
]


@pytest.mark.parametrize("case", MODULE_CASES, ids=[case["name"] for case in MODULE_CASES])
def test_module_endpoints_smoke(client, case):
    method = case["method"].lower()
    path = case["path"]
    payload = case["json"]

    response = getattr(client, method)(path, json=payload) if payload else getattr(client, method)(path)

    assert response.status_code in case["expected_statuses"], (
        f"{case['name']} devolvió {response.status_code}. "
        f"Esperados: {case['expected_statuses']}. "
        f"Revisa ruta/payload/schema."
    )


# NEGATIVOS GENÉRICOS PARA MÓDULOS CON PATH PARAMS
NEGATIVE_CASES = [
    {
        "name": "get_user_invalid_id",
        "method": "get",
        "path": "/api/v1/users/invalid",
        "json": None,
        "expected_statuses": {422},
    },
    {
        "name": "get_notification_invalid_user_id",
        "method": "get",
        "path": "/api/v1/users/invalid/notifications",
        "json": None,
        "expected_statuses": {422},
    },
]


@pytest.mark.parametrize("case", NEGATIVE_CASES, ids=[case["name"] for case in NEGATIVE_CASES])
def test_module_endpoints_negative_validation(client, case):
    method = case["method"].lower()
    path = case["path"]
    payload = case["json"]

    response = getattr(client, method)(path, json=payload) if payload else getattr(client, method)(path)

    assert response.status_code in case["expected_statuses"]