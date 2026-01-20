import json
import os
import pickle
import re

import pandas as pd
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from spacy.language import Language
from tqdm import tqdm

tqdm.pandas()

print("Reading dataset...")
df = pd.read_csv("data/pg_books.csv")
df = pd.DataFrame(df.iloc[:1000])

df["authors"] = (
    df["authors"]
    .apply(json.loads)
    .apply(lambda x: ", ".join(map(lambda y: y["name"], x)))
)
df["subjects"] = df["subjects"].apply(json.loads).apply(lambda x: ", ".join(x))
df["classes"] = df["classes"].apply(json.loads).apply(lambda x: ", ".join(x))
df["subclasses"] = (
    df["subclasses"].apply(json.loads).apply(lambda x: ", ".join(x))
)
df["language_code"] = df["language_code"].apply(lambda x: x[:2])

columns = [
    "title",
    "authors",
    "summary",
    "subjects",
    "classes",
    "subclasses",
]

df_docs = pd.DataFrame()
df_docs["text"] = (
    df[columns]
    .fillna("")
    .astype(str)
    .apply(lambda row: ", ".join(filter(None, row)).strip('"'), axis=1)
)
df_docs["language_code"] = df["language_code"]

NLP_CACHE = {}


def get_nlp(lang: str) -> Language | None:
    if lang not in NLP_CACHE:
        NLP_CACHE[lang] = None
        for type in ["sm", "lg", "trf"]:
            for n in ["web", "news"]:
                model_type = f"{lang}_core_{n}_{type}"
                try:
                    if not spacy.util.is_package(model_type):
                        print(f"Downloading spacy model {model_type}...")
                        os.system(f"python -m spacy download {model_type}")

                    print(f"Loading spacy model {model_type}...")
                    NLP_CACHE[lang] = spacy.load(
                        model_type,
                        disable=[
                            "tagger",
                            "parser",
                            "attribute_ruler",
                            "lemmatizer",
                        ],
                    )
                except Exception:
                    print(f"No type {model_type} for language {lang}")

                if NLP_CACHE.get(lang):
                    print("Model loaded successfully.")
                    break

            if NLP_CACHE.get(lang):
                break

    return NLP_CACHE.get(lang)


def transform_text(text: str, lang: str) -> str:
    """
    Transform recognized named entity to be identified as one word by replacing
    spaces with underscores (_).
    """

    transformed_text = text
    nlp = get_nlp(lang)

    if not nlp:
        return text

    text_ner = nlp(text)
    for ent in reversed(text_ner.ents):
        start = ent.start_char
        end = ent.end_char
        transformed_text = (
            transformed_text[:start]
            + re.sub(
                r"(^|[_\s])the_",
                " the ",
                ent.text.replace(" ", "_"),
                flags=re.IGNORECASE,
            )
            + transformed_text[end:]
        )
    return transformed_text


print("Transforming text with NER...")
df_docs["text"] = df_docs.progress_apply(
    lambda row: transform_text(row["text"], row["language_code"]), axis=1
)

print("Computing TF-IDF...")
tfidf = TfidfVectorizer(max_features=10000)
tfidf_matrix = tfidf.fit_transform(df_docs["text"].fillna(""))

print("Computing Cosine Similarity...")
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

print("Writing cosine similarity matrix to tfidf_matrix.pkl")
os.makedirs("models", exist_ok=True)

with open("models/tfidf_matrix.pkl", "wb") as f:
    pickle.dump(cosine_sim, f)
