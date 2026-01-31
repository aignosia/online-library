import typer

from app.config.db import init_db
from scripts.seed_book_embeddings import seed_book_embeddings
from scripts.seed_books import seed_books
from scripts.seed_default_user import seed_default_user

app = typer.Typer()


@app.command("user")
def run_seed_default_user():
    typer.echo("Seeding default user...")
    seed_default_user()


@app.command("books")
def run_seed_books(
    data: str = typer.Option(
        "",
        "--data",
        "-d",
        exists=True,
        file_okay=True,
        readable=True,
        help="Path to the MarcXML file containing the books to insert to the database (required for 'books')",
    ),
    booknum: int | None = typer.Option(
        None, "--booknum", "-n", help="Number of books to seed"
    ),
):
    typer.echo("Seeding books...")
    seed_books(data, booknum)


@app.command("embeddings")
def run_seed_book_embeddings():
    typer.echo("Seeding book embeddings...")
    seed_book_embeddings()


if __name__ == "__main__":
    init_db()
    app()
    typer.echo("Seeding finished successfully!")
