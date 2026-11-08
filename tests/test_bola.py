from fastapi.testclient import TestClient

from app.models.user import User
from tests.utils import bearer


def test_owner_can_read_own_prediction_log(
    client: TestClient, user_a: User, user_a_token: str, make_log
):
    log = make_log(user_a)

    response = client.get(f"/predict/{log.id}", headers=bearer(user_a_token))

    assert response.status_code == 200
    assert response.json()["id"] == log.id


def test_user_cannot_read_another_users_prediction_log(
    client: TestClient, user_a: User, user_b_token: str, make_log
):
    log = make_log(user_a)

    response = client.get(f"/predict/{log.id}", headers=bearer(user_b_token))

    assert response.status_code == 404


def test_foreign_log_is_indistinguishable_from_nonexistent_log(
    client: TestClient, user_a: User, user_b_token: str, make_log
):
    """Evita enumeração de IDs: 404 idêntico para 'não existe' e 'não é seu'."""
    foreign = client.get(
        f"/predict/{make_log(user_a).id}", headers=bearer(user_b_token)
    )
    missing = client.get("/predict/999999", headers=bearer(user_b_token))

    assert foreign.status_code == missing.status_code == 404
    assert foreign.json() == missing.json()


def test_reading_log_without_token_returns_401(
    client: TestClient, user_a: User, make_log
):
    log = make_log(user_a)

    response = client.get(f"/predict/{log.id}")

    assert response.status_code == 401