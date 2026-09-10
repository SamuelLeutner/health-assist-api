from sqlmodel import Session, select

from app.database import engine, init_db
from app.models.user import User
from app.security.jwt import get_password_hash


def create_initial_user() -> None:
    init_db()
    with Session(engine) as session:
        existing = session.exec(select(User).where(User.username == "admin")).first()
        if existing:
            print("Usuário já existe.")
            return

        session.add(
            User(username="admin", hashed_password=get_password_hash("senha123"))
        )
        session.commit()
        print("Usuário 'admin' criado com sucesso!")


if __name__ == "__main__":
    create_initial_user()
