from sqlmodel import Session

from app.config.db import engine, init_db
from app.users.models import User, UserCreate
from app.users.services import add_user


def seed_default_user():
    init_db()
    session = Session(engine)
    default_user = UserCreate(
        username="johndoe",
        email="john@email.com",
        password="secret123",
        full_name="John Doe",
    )
    if not session.get(User, default_user.username):
        add_user(default_user, session)


if __name__ == "__main__":
    seed_default_user()
