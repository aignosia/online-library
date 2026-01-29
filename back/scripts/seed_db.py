import typer

from scripts.seed_book_embeddings import seed_book_embeddings
from scripts.seed_books import seed_books
from scripts.seed_default_user import seed_default_user

app = typer.Typer()


def run_seed_default_user():
    typer.echo("Inserting default user...")
    seed_default_user()


def run_seed_books(data: str):
    typer.echo("Inserting books...")
    seed_books(data)


def run_seed_book_embeddings(model: str):
    typer.echo("Adding book embeddings...")
    seed_book_embeddings(model)


@app.command()
def run(
    resource: str = typer.Option(
        "all",
        "--resource",
        "-r",
        help="Resources can be : 'user', 'books', 'embeddings'",
    ),
    data: str | None = typer.Option(
        None,
        "--data",
        "-d",
        exists=True,
        file_okay=True,
        readable=True,
        help="Path to the MarcXML file containing the books to insert to the database (required for 'books')",
    ),
    model: str | None = typer.Option(
        None,
        "--model",
        "-m",
        exists=True,
        file_okay=True,
        readable=True,
        help="Path to the TF-IDF vectorizer file (required for 'embeddings')",
    ),
):
    "Run database seed according to the resource selected"
    typer.echo("Starting seeding")
    if resource == "user":
        run_seed_default_user()
    elif resource == "books":
        if not data:
            raise FileNotFoundError("Enter a valid data source file path.")
        run_seed_books(data)
    elif resource == "embeddings":
        if not model:
            raise FileNotFoundError("Enter a valid model file path")
        run_seed_book_embeddings(model)
    else:
        typer.echo(f"Error: uknown resource '{resource}'.", err=True)
        raise typer.Exit(code=1)

    typer.echo("Seeding finished successfully!")


if __name__ == "__main__":
    app()
