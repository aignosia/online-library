import os

import joblib
import pandas as pd
import typer
from sklearn.feature_extraction.text import TfidfVectorizer


def main(out: str, path: str):
    df = pd.read_csv(path)

    print("Computing TF-IDF...")
    tfidf = TfidfVectorizer(max_features=10000)
    tfidf.fit_transform(df["text"].fillna(""))

    print("Writing TF-IDF vectorizer to tfidf_vectorizer.joblib")
    os.makedirs("models", exist_ok=True)
    joblib.dump(tfidf, out)


if __name__ == "__main__":
    typer.run(main)
