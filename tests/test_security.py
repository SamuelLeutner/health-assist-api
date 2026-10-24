from app.models.prediction_log import PredictionLog
from fastapi.testclient import TestClient
from app.models.user import User
from sqlmodel import Session
from app.main import app

VALID_PREDICT_PAYLOAD = {
    "symptoms_description": "Dor de cabeça forte e febre há dois dias.",
    "patient_age": 30,
}


client = TestClient(app)


def test_security_headers_are_present():
    response = client.get("/health")

    assert response.status_code == 200
    headers = response.headers

    assert "X-Content-Type-Options" in headers
    assert headers["X-Content-Type-Options"] == "nosniff"
    assert "X-Frame-Options" in headers
    assert "Strict-Transport-Security" in headers


def test_rate_limiting():
    isolated_client = TestClient(app, client=("10.0.0.99", 50000))

    endpoint = "/auth/token"
    limit = 5

    for _ in range(limit):
        isolated_client.post(endpoint, data={"username": "test", "password": "123"})

    response = isolated_client.post(
        endpoint, data={"username": "test", "password": "123"}
    )
    assert response.status_code == 429


def test_input_validation_malformed_data():
    response = client.post("/auth/token", json={"username": 12345, "password": ""})
    assert response.status_code == 422


def test_authentication_failure():
    response = client.post(
        "/auth/token", data={"username": "usuario_falso", "password": "senha_errada"}
    )
    assert response.status_code in [401, 403]


def test_bola_protection(
    client: TestClient,
    session: Session,
    user_a: User,
    user_b: User,
    user_a_token: str,
    user_b_token: str,
):
    log = PredictionLog(
        user_id=user_a.id,
        input_data="Sintomas confidenciais do usuário A",
        prediction_result="Urgência Baixa",
    )
    session.add(log)
    session.commit()
    session.refresh(log)

    response = client.get(
        f"/predict/{log.id}",
        headers={"Authorization": f"Bearer {user_b_token}"},
    )

    assert response.status_code == 404


def test_security_headers_are_present():
    response = client.get("/health")
    assert response.status_code == 200
    assert "X-Content-Type-Options" in response.headers
    assert "X-Frame-Options" in response.headers


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


def test_predict_endpoint(client, user_a_token):
    response = client.post(
        "/predict/",
        headers={"Authorization": f"Bearer {user_a_token}"},
        json={
            "symptoms_description": "Dor forte no peito e falta de ar súbita.",
            "patient_age": 45,
        },
    )
    assert response.status_code == 200
