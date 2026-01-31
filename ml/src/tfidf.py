from pathlib import Path

import typer

from src.tfidf_preprocessing import preprocess
from src.tfidf_test import test
from src.tfidf_train import train

app = typer.Typer()


@app.command("preprocess")
def run_preprocess(
    booknum: int | None = typer.Option(
        None, "--number", "-n", help="Number of book to add to preprocess."
    ),
    output: Path = typer.Argument(
        help="Path to the output file to write the preprocessed data."
    ),
    source_path: Path = typer.Argument(
        help="Path to the MarcXML file containing the data source of the books."
    ),
):
    preprocess(output, source_path, booknum)


@app.command("train")
def run_train(
    output: Path = typer.Argument(
        help="Path to the output joblib file to write the model."
    ),
    source_path: Path = typer.Argument(
        help="Path to the CSV file containing the training data."
    ),
):
    train(output, source_path)


@app.command("test")
def run_test(
    model_path: Path = typer.Argument(
        help="Path to the TF-IDF Vectorizer joblib file"
    ),
    data_path: Path = typer.Argument(
        help="Path to the data used to test the model."
    ),
    book_id: int = typer.Argument(help="id of the query book."),
    rec_number: int = typer.Option(
        10, "--rec_number", "-r", help="Number of recommendations needed"
    ),
):
    test(model_path, data_path, book_id, rec_number)


if __name__ == "__main__":
    app()
