import os

os.environ.update(
    {
        "PROJECT_NAME": "HealthAssist Test",
        "SECRET_KEY": "test-only-secret-key-with-at-least-32-characters",
        "ALGORITHM": "HS256",
        "ACCESS_TOKEN_EXPIRE_MINUTES": "30",
        "DATABASE_URL": "sqlite://",
    }
)

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402
from sqlmodel import Session, SQLModel, create_engine  # noqa: E402
from sqlmodel.pool import StaticPool  # noqa: E402

from app.database import get_db  # noqa: E402
from app.main import app  # noqa: E402
from app.models.prediction_log import PredictionLog  # noqa: E402
from app.models.user import User  # noqa: E402
from app.security.jwt import get_password_hash  # noqa: E402
from app.security.rate_limit import limiter  # noqa: E402

ALICE_PASSWORD = "alice-pass-123"
BOB_PASSWORD = "bob-pass-123"


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_db_override():
        yield session

    app.dependency_overrides[get_db] = get_db_override
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()


@pytest.fixture(autouse=True)
def reset_rate_limiter():
    limiter.reset()
    yield
    limiter.reset()


def _create_user(session: Session, username: str, password: str) -> User:
    user = User(username=username, hashed_password=get_password_hash(password))
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def _login(client: TestClient, username: str, password: str) -> str:
    response = client.post(
        "/auth/token", data={"username": username, "password": password}
    )
    assert response.status_code == 200
    return response.json()["access_token"]


@pytest.fixture(name="user_a")
def user_a_fixture(session: Session) -> User:
    return _create_user(session, "alice", ALICE_PASSWORD)


@pytest.fixture(name="user_b")
def user_b_fixture(session: Session) -> User:
    return _create_user(session, "bob", BOB_PASSWORD)


@pytest.fixture(name="user_a_token")
def user_a_token_fixture(client: TestClient, user_a: User) -> str:
    return _login(client, user_a.username, ALICE_PASSWORD)


@pytest.fixture(name="user_b_token")
def user_b_token_fixture(client: TestClient, user_b: User) -> str:
    return _login(client, user_b.username, BOB_PASSWORD)


@pytest.fixture(name="make_log")
def make_log_fixture(session: Session):
    def _make_log(owner: User) -> PredictionLog:
        log = PredictionLog(
            user_id=owner.id,
            input_data="Sintomas confidenciais do usuário",
            prediction_result="Urgência Baixa",
        )
        session.add(log)
        session.commit()
        session.refresh(log)
        return log

    return _make_log
