from app.database import SessionLocal
from app.models.user import User
from app.security.jwt import get_password_hash


def create_initial_user():
    db = SessionLocal()

    user = db.query(User).filter(User.username == "admin").first()
    if user:
        print("Usuário já existe.")
        db.close()
        return

    new_user = User(username="admin", hashed_password=get_password_hash("senha123"))

    db.add(new_user)
    db.commit()
    db.close()

    print("Usuário 'admin' criado com sucesso!")


if __name__ == "__main__":
    create_initial_user()
