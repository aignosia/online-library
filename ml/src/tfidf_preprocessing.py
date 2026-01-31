import json
import re
from pathlib import Path

import fugashi
import jieba
import pandas as pd
import tltk
import typer
from konlpy.tag import Kkma
from stop_words import safe_get_stop_words
from tqdm import tqdm
from underthesea import word_tokenize

tqdm.pandas()


def filter_stop_words(lang: str, text: str):
    stop_words = set(safe_get_stop_words(lang))
    words = text.split()
    filtered = [w for w in words if w not in stop_words]
    return " ".join(filtered)


def create_authors_text(authors_col: str):
    authors = json.loads(authors_col)
    authors = list(filter(lambda x: x is not None, authors))
    authors_text = " | ".join(
        author["name"].replace(" ", "_") for author in authors
    )
    return authors_text


def create_metadata_text(metadata_col: str, repetition: int = 1):
    metadata = json.loads(metadata_col)
    metadata = list(filter(lambda x: x is not None, metadata))
    metadata_text = " | ".join(metadata * repetition)
    return metadata_text


def create_tfidf_text(row: pd.Series):
    authors = create_authors_text(row["authors"])
    title = row["title"]
    subjects = create_metadata_text(row["subjects"], 2)
    classes = create_metadata_text(row["classes"], 2)
    subclasses = create_metadata_text(row["subclasses"], 2)
    text = " ".join([authors, title, classes, subclasses, subjects])
    text = re.sub(r"[^a-zA-Z0-9_|\-\s]", "", text.lower())
    text = re.sub(r"\s+", " ", text).strip()
    text = filter_stop_words(row["language_code"][:2], text)
    lc = row["language_code"][:2]
    if lc == "jp":
        text = fugashi.Tagger().parse(text)
    elif lc == "cn":
        text = " ".join(jieba.lcut(text))
    elif lc == "kr":
        text = " ".join(Kkma().morphs(text))
    elif lc == "th":
        pos = tltk.nlp.pos_tag(text)
        text = " ".join([w[0] for piece in pos for w in piece])
    elif lc == "vn":
        text = word_tokenize(text, format="text")
    return text


def preprocess(out: Path, data_source: Path, size: int | None = None):
    typer.echo("Reading dataset...")
    df = pd.read_csv(data_source)

    if size and size >= 0:
        df = pd.DataFrame(df.iloc[:size])

    df["text"] = (
        df.fillna("").astype(str).progress_apply(create_tfidf_text, axis=1)
    )

    typer.echo(f"Writing to {out}...")
    df.to_csv(out, index=False)
