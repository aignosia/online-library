import os
from pathlib import Path

import joblib
import pandas as pd
import typer
from sklearn.feature_extraction.text import TfidfVectorizer


def train(output: Path, data_source: Path):
    df = pd.read_csv(data_source)

    typer.echo("Computing TF-IDF...")
    tfidf = TfidfVectorizer(max_features=5000)
    tfidf.fit(df["text"].fillna(""))

    typer.echo(f"Writing TF-IDF vectorizer to {output}")
    os.makedirs("models", exist_ok=True)
    joblib.dump(tfidf, output)
