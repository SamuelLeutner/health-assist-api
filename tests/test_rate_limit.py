from fastapi.testclient import TestClient

from app.models.user import User
from app.routers.auth import AUTH_RATE_LIMIT
from app.routers.predict import PREDICT_RATE_LIMIT
from tests.utils import VALID_PREDICT_PAYLOAD, bearer


def _limit_per_minute(rule: str) -> int:
    return int(rule.split("/")[0])


def test_login_is_rate_limited_after_configured_attempts(
    client: TestClient, user_a: User
):
    attempts = _limit_per_minute(AUTH_RATE_LIMIT)
    credentials = {"username": "alice", "password": "wrong-password"}

    statuses = [
        client.post("/auth/token", data=credentials).status_code
        for _ in range(attempts + 1)
    ]

    assert statuses[:attempts] == [401] * attempts
    assert statuses[attempts] == 429


def test_predict_is_rate_limited_after_configured_requests(
    client: TestClient, user_a_token: str
):
    allowed = _limit_per_minute(PREDICT_RATE_LIMIT)
    headers = bearer(user_a_token)

    statuses = [
        client.post("/predict/", json=VALID_PREDICT_PAYLOAD, headers=headers).status_code
        for _ in range(allowed + 1)
    ]

    assert statuses[:allowed] == [200] * allowed
    assert statuses[allowed] == 429