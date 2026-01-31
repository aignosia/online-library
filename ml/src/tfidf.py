from pathlib import Path

import typer

from src.tfidf_preprocessing import preprocess
from src.tfidf_test import test_recommendation_model
from src.tfidf_train import train

app = typer.Typer()


@app.command("preprocess")
def run_preprocess(
    booknum: int | None = typer.Option(
        None, "--number", "-n", help="Number of book to add to preprocess."
    ),
    output: Path = typer.Option(
        ...,
        "--output",
        "-o",
        help="Path to the output file to write the preprocessed data.",
    ),
    source_path: Path = typer.Argument(
        help="Path to the MarcXML file containing the data source of the books."
    ),
):
    """Preprocess book dataset to be used to train a TF-IDF vectorizer."""
    typer.echo("Starting preprocessing...")
    preprocess(output, source_path, booknum)
    typer.echo("Preprocessing finished successfully!")


@app.command("train")
def run_train(
    output: Path = typer.Option(
        ...,
        "--output",
        "-o",
        help="Path to the output joblib file to write the model.",
    ),
    source_path: Path = typer.Argument(
        help="Path to the CSV file containing the training data."
    ),
):
    """Train a TF-IDF vectorizer using the preprocessed data."""
    typer.echo("Starting training...")
    train(output, source_path)
    typer.echo("Training finished successfully!")


@app.command("test")
def run_test(
    model_path: Path = typer.Option(
        ..., "--model", "-m", help="Path to the TF-IDF Vectorizer file (joblib)"
    ),
    data_path: Path = typer.Option(
        ..., "--data", "-d", help="Path to the data used to test the model."
    ),
    rec_number: int = typer.Option(
        10, "--rec-num", "-r", help="Number of recommendations needed"
    ),
    book_id: int = typer.Argument(help="ID of the query book."),
):
    """Test the trained TF-IDF vectorizer on the data."""
    typer.echo("Starting test...")
    test_recommendation_model(model_path, data_path, rec_number, book_id)
    typer.echo("Test finished successfully!")


if __name__ == "__main__":
    app()
