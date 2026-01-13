from pathlib import Path

import typer

from scripts.seed_books import seed_books
from scripts.seed_default_user import seed_default_user

app = typer.Typer()


def run_seed_default_user():
    typer.echo("Inserting default user...")
    seed_default_user()


def run_seed_books(file_path: Path):
    typer.echo("Inserting books...")
    seed_books(file_path)


@app.command()
def run(
    resource: str = typer.Option(
        "all",
        "--resource",
        "-r",
        help="Resources can be : 'user', 'books', 'all'",
    ),
    file: str | None = typer.Option(
        None,
        "--file",
        "-f",
        exists=True,
        file_okay=True,
        readable=True,
        help="Path to the MarcXML file containing the books to insert to the database (required for 'books')",
    ),
):
    "Run database seed according to the resource selected"
    if resource == "user":
        seed_default_user()
    elif resource == "books":
        seed_books(Path(file if file else "downloads/pgmarc.xml"))
    elif resource == "all":
        seed_default_user()
        seed_books(Path(file if file else "downloads/pgmarc.xml"))
    else:
        typer.echo(f"Error: uknown resource '{resource}'.", err=True)
        raise typer.Exit(code=1)

    typer.echo("Seeding finished successfully!")


if __name__ == "__main__":
    app()
