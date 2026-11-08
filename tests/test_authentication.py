from datetime import timedelta

import jwt
import pytest
from fastapi.testclient import TestClient

from app.models.user import User
from tests.utils import VALID_PREDICT_PAYLOAD, bearer, forge_token


def test_login_with_valid_credentials_returns_bearer_token(
    client: TestClient, user_a: User
):
    response = client.post(
        "/auth/token", data={"username": "alice", "password": "alice-pass-123"}
    )

    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "bearer"
    assert body["access_token"]


@pytest.mark.parametrize(
    ("username", "password"),
    [
        ("alice", "wrong-password"),
        ("ghost-user", "whatever-password"),
    ],
    ids=["wrong-password", "unknown-user"],
)
def test_login_with_invalid_credentials_returns_401(
    client: TestClient, user_a: User, username: str, password: str
):
    response = client.post(
        "/auth/token", data={"username": username, "password": password}
    )

    assert response.status_code == 401
    assert response.headers["WWW-Authenticate"] == "Bearer"


def test_protected_endpoint_without_token_returns_401(client: TestClient):
    response = client.post("/predict/", json=VALID_PREDICT_PAYLOAD)

    assert response.status_code == 401


def test_protected_endpoint_rejects_garbage_token(client: TestClient):
    response = client.post(
        "/predict/", json=VALID_PREDICT_PAYLOAD, headers=bearer("not-a-jwt")
    )

    assert response.status_code == 401


def test_protected_endpoint_rejects_expired_token(client: TestClient, user_a: User):
    expired = forge_token("alice", expires_in=timedelta(minutes=-1))

    response = client.post(
        "/predict/", json=VALID_PREDICT_PAYLOAD, headers=bearer(expired)
    )

    assert response.status_code == 401


def test_protected_endpoint_rejects_token_signed_with_another_key(
    client: TestClient, user_a: User
):
    forged = forge_token("alice", key="another-secret-key-with-32-characters!!")

    response = client.post(
        "/predict/", json=VALID_PREDICT_PAYLOAD, headers=bearer(forged)
    )

    assert response.status_code == 401


def test_protected_endpoint_rejects_unsigned_token(client: TestClient, user_a: User):
    unsigned = jwt.encode({"sub": "alice"}, None, algorithm="none")

    response = client.post(
        "/predict/", json=VALID_PREDICT_PAYLOAD, headers=bearer(unsigned)
    )

    assert response.status_code == 401


def test_protected_endpoint_rejects_token_of_nonexistent_user(client: TestClient):
    token = forge_token("deleted-user")

    response = client.post(
        "/predict/", json=VALID_PREDICT_PAYLOAD, headers=bearer(token)
    )

    assert response.status_code == 401