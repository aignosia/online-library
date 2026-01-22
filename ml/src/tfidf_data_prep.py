import json
import re

import pandas as pd
import spacy
import typer
from spacy.tokens import Doc
from tqdm import tqdm

NLP_CACHE = {}


def merge_entity(doc: Doc) -> str:
    with doc.retokenize() as retokenizer:
        for ent in doc.ents:
            new_text = ent.text.replace(" ", "_")
            retokenizer.merge(ent, attrs={"LEMMA": new_text})

    return " ".join([t.lemma_ if t.lemma_ != t.text else t.text for t in doc])


def main(out: str, path: str, size: int | None = None):
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
        .apply(lambda row: " | ".join(filter(None, row)), axis=1)
    )
    df_docs["text"] = df_docs["text"].str.replace('"', "")

    print("Merging entity names using NER...")
    nlp = spacy.load("xx_ent_wiki_sm")
    docs = nlp.pipe(df_docs["text"], n_process=-1, batch_size=50)
    df_docs["text"] = pd.Series(
        [merge_entity(doc) for doc in tqdm(docs, total=len(df_docs))]
    )

    df_docs["text"] = df_docs["text"].apply(
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

    df["text"] = df_docs["text"]
    print(f"Writing to {out}...")
    df.to_csv(out, index=False)


if __name__ == "__main__":
    typer.run(main)
