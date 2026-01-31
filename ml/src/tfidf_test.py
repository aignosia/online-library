import json
from pathlib import Path

import joblib
import pandas as pd
import typer
from sklearn.metrics.pairwise import cosine_similarity


def test_recommendation_model(
    model_path: Path,
    data_path: Path,
    rec_number: int,
    book_id: int,
):
    typer.echo("Loading data...")
    df = pd.read_csv(data_path)
    df["authors"] = (
        df["authors"]
        .apply(json.loads)
        .apply(lambda x: ", ".join(map(lambda y: y["name"], x)))
    )

    if book_id >= len(df):
        raise Exception(
            f"The id you provided is too large. Set it to be less than your dataset\
: \nthe maximum id in your dataset is {len(df) - 1}"
        )

    typer.echo("Loading TF-IDF vectorizer...")
    tfidf = joblib.load(model_path)
    typer.echo("Computing embeddings...")
    tfidf_matrix = tfidf.transform(df["text"].fillna(""))
    book_vector = tfidf_matrix[book_id]
    typer.echo("Computing cosine similarities...")
    df["cosine_sim"] = cosine_similarity(book_vector, tfidf_matrix).flatten()
    typer.echo("Sorting recommandations...")
    book = df.iloc[[book_id]]
    recommendations = df.sort_values(by="cosine_sim", ascending=False).iloc[
        1 : rec_number + 1
    ]
    typer.echo(f"Book:\n{book[['authors', 'title']]}")
    typer.echo(f"Recommendations:\n{recommendations[['authors', 'title']]}")
