from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException

from app.features.auth.service import AuthService, active_tokens
from app.features.auth.schemas import LoginRequest
from app.core.shared_schemas import UserCreate
from app.db.models import User, Role


def make_query_mock(first_result=None, all_result=None):
    query = MagicMock()
    query.filter.return_value = query
    query.first.return_value = first_result
    query.all.return_value = all_result if all_result is not None else []
    return query


def test_login_success():
    db = MagicMock()
    user = User(
        id=1,
        email="test@example.com",
        password="secret123",
        first_name="Test",
        last_name="User",
        organization="UC3M",
        is_verified=True
    )

    db.query.return_value.filter.return_value.first.return_value = user

    service = AuthService(db)
    payload = LoginRequest(email="test@example.com", password="secret123")

    active_tokens.clear()
    response = service.login(payload)

    assert response.access_token is not None
    assert response.token_type == "bearer"
    assert active_tokens[response.access_token] == 1


def test_login_invalid_credentials_when_user_not_found():
    db = MagicMock()
    db.query.return_value.filter.return_value.first.return_value = None

    service = AuthService(db)
    payload = LoginRequest(email="missing@example.com", password="secret123")

    with pytest.raises(HTTPException) as exc:
        service.login(payload)

    assert exc.value.status_code == 401
    assert exc.value.detail == "Credenciales inválidas"


def test_login_invalid_credentials_when_password_is_wrong():
    db = MagicMock()
    user = User(
        id=1,
        email="test@example.com",
        password="other-password",
        first_name="Test",
        last_name="User",
        organization="UC3M",
    )

    db.query.return_value.filter.return_value.first.return_value = user

    service = AuthService(db)
    payload = LoginRequest(email="test@example.com", password="secret123")

    with pytest.raises(HTTPException) as exc:
        service.login(payload)

    assert exc.value.status_code == 401
    assert exc.value.detail == "Credenciales inválidas"


def test_register_success():
    db = MagicMock()

    existing_user_query = make_query_mock(first_result=None)
    roles_query = make_query_mock(all_result=[(1,), (2,)])

    user = User(
        id=10,
        email="new@example.com",
        password="secret123",
        first_name="New",
        last_name="User",
        organization="UC3M",
    )

    db.query.side_effect = [existing_user_query, roles_query]

    def add_side_effect(obj):
        if isinstance(obj, User):
            obj.id = 10

    db.add.side_effect = add_side_effect
    db.refresh.side_effect = lambda obj: None
    db.flush.side_effect = lambda: None
    db.commit.side_effect = lambda: None

    service = AuthService(db)
    payload = UserCreate(
        email="new@example.com",
        password="secret123",
        first_name="New",
        last_name="User",
        organization="UC3M",
        role_ids=[1, 2],
    )

    response = service.register(payload)

    assert response.id == 10
    assert response.email == payload.email
    assert response.first_name == payload.first_name
    assert response.last_name == payload.last_name
    assert response.organization == payload.organization
    assert response.role_ids == [1, 2]
    assert db.commit.called
    assert db.refresh.called


def test_register_duplicate_email():
    db = MagicMock()
    existing_user = User(
        id=1,
        email="existing@example.com",
        password="secret123",
        first_name="Existing",
        last_name="User",
        organization="UC3M",
    )

    db.query.return_value.filter.return_value.first.return_value = existing_user

    service = AuthService(db)
    payload = UserCreate(
        email="existing@example.com",
        password="secret123",
        first_name="New",
        last_name="User",
        organization="UC3M",
        role_ids=[1],
    )

    with pytest.raises(HTTPException) as exc:
        service.register(payload)

    assert exc.value.status_code == 409
    assert exc.value.detail == "El email ya está registrado"


def test_ensure_roles_exist_success():
    db = MagicMock()
    db.query.return_value.filter.return_value.all.return_value = [(1,), (2,)]

    service = AuthService(db)

    service._ensure_roles_exist([1, 2])


def test_ensure_roles_exist_with_missing_role():
    db = MagicMock()
    db.query.return_value.filter.return_value.all.return_value = [(1,)]

    service = AuthService(db)

    with pytest.raises(HTTPException) as exc:
        service._ensure_roles_exist([1, 2])

    assert exc.value.status_code == 400
    assert exc.value.detail == "Roles no encontrados: [2]"


def test_ensure_roles_exist_with_empty_list():
    db = MagicMock()
    service = AuthService(db)

    service._ensure_roles_exist([])

    db.query.assert_not_called()