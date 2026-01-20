import json
import os
import re

import pandas as pd
import spacy
import typer
from spacy.language import Language
from tqdm import tqdm

tqdm.pandas()

NLP_CACHE = {}


def get_nlp(lang: str) -> Language | None:
    if lang not in NLP_CACHE:
        NLP_CACHE[lang] = None
        for n in ["web", "news"]:
            model_type = f"{lang}_core_{n}_sm"
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


def entity_merge(doc):
    with doc.retokenize() as retokenizer:
        for ent in doc.ents:
            new_text = ent.text.replace(" ", "_")
            retokenizer.merge(ent, attrs={"LEMMA": new_text})

    return " ".join([t.lemma_ if t.lemma_ != t.text else t.text for t in doc])


def process_data(out: str, path: str, size: int | None = None):
    print("Reading dataset...")
    df = pd.read_csv(path)

    if size and size >= 0:
        df = pd.DataFrame(df.iloc[:size])

    df_docs = pd.DataFrame()
    df_docs["authors"] = (
        df["authors"]
        .apply(json.loads)
        .apply(lambda x: ", ".join(map(lambda y: y["name"], x)))
    )
    df_docs["subjects"] = (
        df["subjects"].apply(json.loads).apply(lambda x: ", ".join(x))
    )
    df_docs["classes"] = (
        df["classes"].apply(json.loads).apply(lambda x: ", ".join(x))
    )
    df_docs["subclasses"] = (
        df["subclasses"].apply(json.loads).apply(lambda x: ", ".join(x))
    )
    df_docs["language_code"] = df["language_code"].apply(lambda x: x[:2])

    columns = [
        "title",
        "authors",
        "summary",
        "subjects",
        "classes",
        "subclasses",
    ]

    df_docs["text"] = (
        df[columns]
        .fillna("")
        .astype(str)
        .apply(lambda row: ", ".join(filter(None, row)), axis=1)
    )
    df_docs["text"] = df_docs["text"].str.replace('"', "")
    df_docs["language_code"] = df["language_code"].apply(lambda r: r[:2])

    print("Transforming text with NER...")
    results = []
    for lang, group in df_docs.groupby("language_code"):
        nlp = get_nlp(str(lang))
        if nlp:
            docs = nlp.pipe(group["text"], n_process=-1, batch_size=50)
            group_results = [
                entity_merge(doc)
                for doc in tqdm(docs, total=len(group), desc=f" {lang}")
            ]
            results.append(pd.Series(group_results, index=group.index))
        else:
            results.append(group["text"])

    results = pd.concat(results).sort_index()
    results = results.apply(
        lambda r: re.sub(
            r"\s+",
            " ",
            re.sub(
                r"(^|[_\s])the_",
                " the ",
                r,
                flags=re.IGNORECASE,
            ),
        ).strip()
    )

    df["text"] = results
    print(f"Writing to {out}...")
    df.to_csv(out, index=False)


if __name__ == "__main__":
    typer.run(process_data)
