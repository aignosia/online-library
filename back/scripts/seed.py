import typer

from app.config.db import init_db
from scripts.seed_book_embeddings import seed_book_embeddings
from scripts.seed_books import seed_books
from scripts.seed_default_user import seed_default_user

init_db()

app = typer.Typer()


@app.command("user")
def run_seed_default_user():
    """Seed default user to database (require setting environment variables)."""

    typer.echo("Seeding default user...")
    seed_default_user()
    typer.echo("Seeding finished successfully!")


@app.command("books")
def run_seed_books(
    source_file: str = typer.Option(
        ...,
        "--source",
        "-s",
        exists=True,
        file_okay=True,
        readable=True,
        help="Path to the MarcXML source file containing the books to insert",
    ),
    booknum: int | None = typer.Option(
        None, "--number", "-n", help="Number of books to seed"
    ),
):
    """Seed books from MarcXML source file to database (require setting environment variables)."""

    typer.echo("Seeding books...")
    seed_books(source_file, booknum)
    typer.echo("Seeding finished successfully!")


@app.command("embeddings")
def run_seed_book_embeddings():
    """Seed book embeddings for seeded books (require setting environment variables)."""

    typer.echo("Seeding book embeddings...")
    seed_book_embeddings()
    typer.echo("Seeding finished successfully!")


if __name__ == "__main__":
    app()
