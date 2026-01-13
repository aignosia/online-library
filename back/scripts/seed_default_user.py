import typer
from sqlmodel import Session

from app.config.db import engine, init_db
from app.users.models import User, UserCreate
from app.users.services import add_user

init_db()
session = Session(engine)


def seed_default_user():
    """
    Add a default user to the database so that testing does not
    require creating a new account.
    """
    default_user = UserCreate(
        username="johndoe",
        password="secret123",
        full_name="John Doe",
    )
    typer.echo(f"""Default user credentials:
        username: {default_user.username}
        password: {default_user.password}
        full_name: {default_user.full_name}""")

    if session.get(User, default_user.username):
        typer.echo("Default user seeding skipped: user already exists")
    else:
        add_user(default_user, session)


if __name__ == "__main__":
    seed_default_user()
