from fastapi.testclient import TestClient
from sqlmodel import Session

from app.models.prediction_log import PredictionLog
from app.models.user import User

VALID_PREDICT_PAYLOAD = {
    "symptoms_description": "Dor de cabeça forte e febre há dois dias.",
    "patient_age": 30,
}


def test_predict_without_token_is_rejected(client: TestClient):
    response = client.post("/predict/", json=VALID_PREDICT_PAYLOAD)

    assert response.status_code == 401


def test_user_cannot_access_another_users_prediction_log(
    client: TestClient,
    session: Session,
    user_a: User,
    user_b: User,
    user_a_token: str,
    user_b_token: str,
):
    log = PredictionLog(
        user_id=user_a.id,
        input_data="febre alta",
        prediction_result="Urgência Moderada",
    )
    session.add(log)
    session.commit()
    session.refresh(log)

    response = client.get(
        f"/predict/{log.id}",
        headers={"Authorization": f"Bearer {user_b_token}"},
    )
    assert response.status_code == 404

    own_response = client.get(
        f"/predict/{log.id}",
        headers={"Authorization": f"Bearer {user_a_token}"},
    )
    assert own_response.status_code == 200
    assert own_response.json()["id"] == log.id


def test_predict_rejects_unexpected_extra_field(client: TestClient, user_a_token: str):
    payload = {**VALID_PREDICT_PAYLOAD, "is_admin": True}

    response = client.post(
        "/predict/",
        json=payload,
        headers={"Authorization": f"Bearer {user_a_token}"},
    )

    assert response.status_code == 422
