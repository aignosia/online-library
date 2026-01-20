import json

import joblib
import pandas as pd
import typer
from sklearn.metrics.pairwise import cosine_similarity


def process_data(book_id: int, path: str):
    print("Loading data...")
    df = pd.read_csv(path)
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

    print("Loading TF-IDF vectorizer...")
    tfidf = joblib.load("models/tfidf_vectorizer.joblib")
    print("Computing embeddings...")
    tfidf_matrix = tfidf.transform(df["text"].fillna(""))
    book_vector = tfidf_matrix[book_id]
    print("Computing cosine similarities...")
    df["cosine_sim"] = cosine_similarity(book_vector, tfidf_matrix).flatten()
    print("Sorting recommandations...")
    recommendations = df.sort_values(by="cosine_sim", ascending=False).iloc[
        1:11
    ]
    return df.iloc[[book_id]], recommendations


def main(book_id: int, path: str):
    book, recommendations = process_data(book_id, path)
    print(f"Book:\n{book[['authors', 'title']]}")
    print(f"Recommendations:\n{recommendations[['authors', 'title']]}")


if __name__ == "__main__":
    typer.run(main)
