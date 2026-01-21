import json

import joblib
import pandas as pd
import typer
from sklearn.metrics.pairwise import cosine_similarity


def process_data(model_path: str, data_path: str, book_id: int):
    print("Loading data...")
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

    print("Loading TF-IDF vectorizer...")
    tfidf = joblib.load(model_path)
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


def main(model_path: str, data_path: str, book_id: int):
    book, recommendations = process_data(model_path, data_path, book_id)
    print(f"Book:\n{book[['authors', 'title']]}")
    print(f"Recommendations:\n{recommendations[['authors', 'title']]}")


if __name__ == "__main__":
    typer.run(main)
