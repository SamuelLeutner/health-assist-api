import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.database import get_db
from app.main import app
from app.models.user import User
from app.security.jwt import get_password_hash


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


@pytest.fixture(name="user_a")
def user_a_fixture(session: Session) -> User:
    user = User(username="alice", hashed_password=get_password_hash("alice-pass-123"))
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@pytest.fixture(name="user_b")
def user_b_fixture(session: Session) -> User:
    user = User(username="bob", hashed_password=get_password_hash("bob-pass-123"))
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@pytest.fixture(name="user_a_token")
def user_a_token_fixture(client: TestClient, user_a: User) -> str:
    response = client.post(
        "/auth/token", data={"username": "alice", "password": "alice-pass-123"}
    )
    assert response.status_code == 200
    return response.json()["access_token"]


@pytest.fixture(name="user_b_token")
def user_b_token_fixture(client: TestClient, user_b: User) -> str:
    response = client.post(
        "/auth/token", data={"username": "bob", "password": "bob-pass-123"}
    )
    assert response.status_code == 200
    return response.json()["access_token"]
