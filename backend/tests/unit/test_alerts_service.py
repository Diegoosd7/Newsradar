from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException

from app.features.alerts.service import AlertsService
from app.features.alerts.schemas import AlertCreate, AlertUpdate


class FakeUser:
    def __init__(self, id):
        self.id = id


class FakeAlert:
    def __init__(self, id=1, user_id=1, name="Alert", cron_expression="0 * * * *"):
        self.id = id
        self.user_id = user_id
        self.name = name
        self.cron_expression = cron_expression


def test_ensure_user_exists_success():
    db = MagicMock()
    user = FakeUser(id=1)
    db.query.return_value.filter.return_value.first.return_value = user

    service = AlertsService(db)
    result = service._ensure_user_exists(1)

    assert result == user


def test_ensure_user_exists_not_found():
    db = MagicMock()
    db.query.return_value.filter.return_value.first.return_value = None

    service = AlertsService(db)

    with pytest.raises(HTTPException) as exc:
        service._ensure_user_exists(999)

    assert exc.value.status_code == 404
    assert exc.value.detail == "Usuario no encontrado"


def test_get_alert_for_user_or_404_success():
    db = MagicMock()
    service = AlertsService(db)

    alert = FakeAlert(id=7, user_id=1)

    with patch.object(service, "_ensure_user_exists", return_value=FakeUser(1)):
        db.query.return_value.filter.return_value.first.return_value = alert
        result = service._get_alert_for_user_or_404(1, 7)

    assert result == alert


def test_get_alert_for_user_or_404_not_found():
    db = MagicMock()
    service = AlertsService(db)

    with patch.object(service, "_ensure_user_exists", return_value=FakeUser(1)):
        db.query.return_value.filter.return_value.first.return_value = None

        with pytest.raises(HTTPException) as exc:
            service._get_alert_for_user_or_404(1, 999)

    assert exc.value.status_code == 404
    assert exc.value.detail == "Alerta no encontrada para el usuario"


def test_create_user_alert_limit_reached():
    db = MagicMock()
    service = AlertsService(db)

    payload = AlertCreate(
        name="Tech Alert",
        descriptors=["ai", "robotics"],
        categories=[{"code": "tech", "label": "Technology"}],
        cron_expression="0 * * * *",
    )

    with patch.object(service, "_ensure_user_exists", return_value=FakeUser(1)):
        db.query.return_value.filter.return_value.count.return_value = 20

        with pytest.raises(HTTPException) as exc:
            service.create_user_alert(1, payload)

    assert exc.value.status_code == 400
    assert exc.value.detail == "Límite máximo de 20 alertas alcanzado para este usuario."


def test_create_user_alert_success():
    db = MagicMock()
    service = AlertsService(db)

    payload = AlertCreate(
        name="Tech Alert",
        descriptors=["ai", "robotics"],
        categories=[{"code": "tech", "label": "Technology"}],
        cron_expression="0 * * * *",
    )

    with patch.object(service, "_ensure_user_exists", return_value=FakeUser(1)), \
         patch.object(service, "_replace_descriptors") as mock_replace_descriptors, \
         patch.object(service, "_replace_categories") as mock_replace_categories, \
         patch.object(service, "_to_response", return_value={"id": 5, "user_id": 1, "name": "Tech Alert"}):

        db.query.return_value.filter.return_value.count.return_value = 3

        def add_side_effect(obj):
            obj.id = 5

        db.add.side_effect = add_side_effect
        db.flush.side_effect = lambda: None
        db.commit.side_effect = lambda: None
        db.refresh.side_effect = lambda obj: None

        response = service.create_user_alert(1, payload)

    assert response["id"] == 5
    mock_replace_descriptors.assert_called_once_with(5, ["ai", "robotics"])
    mock_replace_categories.assert_called_once_with(5, payload.categories)
    assert db.commit.called
    assert db.refresh.called


def test_update_user_alert_partial_payload():
    db = MagicMock()
    service = AlertsService(db)

    alert = FakeAlert(id=7, user_id=1, name="Old Name", cron_expression="0 * * * *")
    payload = AlertUpdate(name="New Name")

    with patch.object(service, "_get_alert_for_user_or_404", return_value=alert), \
         patch.object(service, "_to_response", return_value={"id": 7, "name": "New Name"}):

        response = service.update_user_alert(1, 7, payload)

    assert response["id"] == 7
    assert alert.name == "New Name"
    assert db.commit.called
    assert db.refresh.called


def test_update_user_alert_descriptors_and_categories():
    db = MagicMock()
    service = AlertsService(db)

    alert = FakeAlert(id=7, user_id=1, name="Old Name", cron_expression="0 * * * *")
    payload = AlertUpdate(
        descriptors=["cloud", "devops"],
        categories=[{"code": "it", "label": "IT"}],
        cron_expression="*/30 * * * *",
    )

    with patch.object(service, "_get_alert_for_user_or_404", return_value=alert), \
         patch.object(service, "_replace_descriptors") as mock_replace_descriptors, \
         patch.object(service, "_replace_categories") as mock_replace_categories, \
         patch.object(service, "_to_response", return_value={"id": 7}):

        service.update_user_alert(1, 7, payload)

    mock_replace_descriptors.assert_called_once_with(7, ["cloud", "devops"])
    mock_replace_categories.assert_called_once()

    args, _ = mock_replace_categories.call_args
    assert args[0] == 7
    assert len(args[1]) == 1

    category = args[1][0]
    if isinstance(category, dict):
        assert category["code"] == "it"
        assert category["label"] == "IT"
    else:
        assert category.code == "it"
        assert category.label == "IT"

    assert alert.cron_expression == "*/30 * * * *"
    assert db.commit.called
    assert db.refresh.called

def test_delete_user_alert_success():
    db = MagicMock()
    service = AlertsService(db)

    delete_query = MagicMock()
    delete_query.filter.return_value = delete_query
    delete_query.delete.return_value = None

    db.query.return_value = delete_query

    with patch.object(service, "_get_alert_for_user_or_404", return_value=FakeAlert(id=7, user_id=1)):
        service.delete_user_alert(1, 7)

    assert db.commit.called


def test_suggest_keywords_with_ai_without_api_key():
    db = MagicMock()
    service = AlertsService(db)

    with patch("app.features.alerts.service.os.getenv", return_value=None):
        with pytest.raises(HTTPException) as exc:
            service.suggest_keywords_with_ai("ia")

    assert exc.value.status_code == 500
    assert exc.value.detail == "Falta la API Key de Gemini en el entorno."


def test_suggest_keywords_with_ai_success_and_limit_10():
    db = MagicMock()
    service = AlertsService(db)

    fake_response = MagicMock()
    fake_response.text = """
    ["uno", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve", "diez", "once"]
    """

    fake_model_info = MagicMock()
    fake_model_info.supported_generation_methods = ["generateContent"]
    fake_model_info.name = "models/fake-gemini"

    fake_model = MagicMock()
    fake_model.generate_content.return_value = fake_response

    with patch("app.features.alerts.service.os.getenv", return_value="fake-key"), \
         patch("app.features.alerts.service.genai.configure"), \
         patch("app.features.alerts.service.genai.list_models", return_value=[fake_model_info]), \
         patch("app.features.alerts.service.genai.GenerativeModel", return_value=fake_model):

        result = service.suggest_keywords_with_ai("ia")

    assert isinstance(result, list)
    assert len(result) == 10
    assert result[0] == "uno"
    assert result[-1] == "diez"