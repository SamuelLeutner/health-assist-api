from sqlmodel import Session, select

from app.database import engine, init_db
from app.models.user import User
from app.security.jwt import get_password_hash


def create_initial_users() -> None:
    init_db()
    with Session(engine) as session:
        # 1. Verifica/Cria o Admin
        if not session.exec(select(User).where(User.username == "admin")).first():
            session.add(
                User(username="admin", hashed_password=get_password_hash("senha123"))
            )
            print("Usuário 'admin' criado com sucesso!")
        else:
            print("Usuário 'admin' já existe.")

        # 2. Verifica/Cria o Usuário Comum
        common_username = "John Doe" 
        if not session.exec(select(User).where(User.username == common_username)).first():
            session.add(
                User(username=common_username, hashed_password=get_password_hash("senha123"))
            )
            print(f"Usuário comum '{common_username}' criado com sucesso!")
        else:
            print(f"Usuário comum '{common_username}' já existe.")

        session.commit()


if __name__ == "__main__":
    create_initial_users()
