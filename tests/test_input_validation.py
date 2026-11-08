import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app.models.prediction_log import PredictionLog
from app.models.user import User
from tests.utils import VALID_PREDICT_PAYLOAD, bearer


def test_valid_payload_returns_prediction_and_persists_log(
    client: TestClient, session: Session, user_a: User, user_a_token: str
):
    response = client.post(
        "/predict/", json=VALID_PREDICT_PAYLOAD, headers=bearer(user_a_token)
    )

    assert response.status_code == 200
    assert set(response.json()) == {
        "status",
        "triage_category",
        "confidence",
        "message",
    }
    logs = session.exec(
        select(PredictionLog).where(PredictionLog.user_id == user_a.id)
    ).all()
    assert len(logs) == 1
    assert logs[0].input_data == VALID_PREDICT_PAYLOAD["symptoms_description"]


@pytest.mark.parametrize(
    "invalid_fields",
    [
        {"is_admin": True},
        {"patient_age": -1},
        {"patient_age": 121},
        {"patient_age": "trinta"},
        {"symptoms_description": "curto"},
        {"symptoms_description": 12345678901},
    ],
    ids=[
        "extra-field",
        "age-below-range",
        "age-above-range",
        "age-wrong-type",
        "description-too-short",
        "description-wrong-type",
    ],
)
def test_predict_rejects_invalid_payload(
    client: TestClient, user_a_token: str, invalid_fields: dict
):
    payload = {**VALID_PREDICT_PAYLOAD, **invalid_fields}

    response = client.post("/predict/", json=payload, headers=bearer(user_a_token))

    assert response.status_code == 422


@pytest.mark.parametrize("missing_field", list(VALID_PREDICT_PAYLOAD))
def test_predict_rejects_missing_required_field(
    client: TestClient, user_a_token: str, missing_field: str
):
    payload = {k: v for k, v in VALID_PREDICT_PAYLOAD.items() if k != missing_field}

    response = client.post("/predict/", json=payload, headers=bearer(user_a_token))

    assert response.status_code == 422


def test_login_rejects_json_body_instead_of_form(client: TestClient):
    response = client.post("/auth/token", json={"username": "alice", "password": "x"})

    assert response.status_code == 422


def test_login_rejects_form_without_password(client: TestClient):
    response = client.post("/auth/token", data={"username": "alice"})

    assert response.status_code == 422