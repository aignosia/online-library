import os
from pathlib import Path

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer


def train(output: Path, data_source: Path):
    df = pd.read_csv(data_source)

    print("Computing TF-IDF...")
    tfidf = TfidfVectorizer(max_features=5000)
    tfidf.fit(df["text"].fillna(""))

    print(f"Writing TF-IDF vectorizer to {output}")
    os.makedirs("models", exist_ok=True)
    joblib.dump(tfidf, output)
