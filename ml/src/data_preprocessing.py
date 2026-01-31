import json
import re
from pathlib import Path
from typing import Any

import pandas as pd
import typer
from pymarc import Field, Record, map_xml

app = typer.Typer()

with open("src/loc_classification.json", "r") as f:
    class_mapping = json.load(f)


def get_fields_value(fields_list: list[Field]) -> list[str]:
    """
    Extracts the raw text value from a list of MARC fields.

    Args:
        fields_list: List of pymarc Field objects.

    Returns:
        A list of strings representing the field values.
    """
    return list(map(lambda x: x.value(), fields_list))


def get_book_authors(record: Record):
    """
    Extracts and processes authors from a MARC record.

    Parses tags 100, 110, 111, and 700 to extract name, first name,
    lifespans, and fuller name. Also handles entity caching.

    Args:
        record: The MARC Record object to analyze.

    Returns:
        A list of Author objects.
    """
    authors_fields = record.get_fields("100", "110", "111", "700")

    authors = []
    for author in authors_fields:
        name_sf = author.get_subfields("a")
        name = name_sf[0].split(", ") if len(name_sf) > 0 else []
        lastname = (
            re.sub(r"[^a-zA-ZÀ-ÿ\s\-]", "", name[0]) if len(name) > 0 else None
        )
        firstname = (
            re.sub(r"[^a-zA-ZÀ-ÿ\s\-]", "", name[1]) if len(name) > 1 else None
        )

        lifespan_sf = author.get_subfields("d")
        lifespan = lifespan_sf[0].split("-") if len(lifespan_sf) > 0 else []
        birth_year = lifespan[0] if len(lifespan) > 0 else None
        death_year = lifespan[1] if len(lifespan) > 1 else None

        if not firstname and not lastname:
            continue

        name = firstname if firstname else ""
        name += " " + lastname if lastname else ""

        authors.append(
            {
                "name": name.strip(),
                "birth_date": birth_year,
                "death_date": death_year,
            }
        )

    return {"authors": json.dumps(authors)}


def get_book_publisher(record: Record):
    """
    Extracts the publisher from a MARC record.

    Args:
        record: The MARC record.

    Returns:
        A Publisher object or None if no information is found.
    """
    publisher_name = re.sub(r"[^a-zA-ZÀ-ÿ\s\-]", "", record.publisher)
    if not publisher_name:
        return {"publisher": None}

    return {"publisher": publisher_name}


def get_book_subjects(record: Record):
    """
    Extracts subjects (keywords) from a MARC record via tag 653.

    Args:
        record: The MARC record.

    Returns:
        A list of Subject objects.
    """
    subject_names = get_fields_value(record.get_fields("653"))
    subjects = []
    for subject_name in subject_names:
        subjects.append(subject_name)

    return {"subjects": json.dumps(subjects)}


def get_book_serie(record: Record):
    """
    Extracts the collection/series from a MARC record via tag 490.

    Args:
        record: The MARC record.

    Returns:
        A Serie object or None.
    """
    serie_field = next(iter(record.get_fields("490")), None)
    if not serie_field:
        return {"serie": None}

    serie_name = serie_field.value()

    return {"serie": serie_name}


def get_book_subclasses(codes: list[str], mapping: Any):
    """
    Maps classification codes (LOC) to Subclass objects.

    Args:
        codes: List of extracted classification codes (tag 050).
        mapping: Mapping dictionary loaded from JSON.

    Returns:
        A list of Subclass objects associated with their respective BookClass.
    """
    classes = []
    subclasses = []
    class_name = None
    for code in codes:
        class_mapping = next(
            filter(lambda x: x.get("code") == code[0], mapping), None
        )
        if not class_mapping:
            continue

        class_name = class_mapping.get("name")
        if class_name and class_name not in classes:
            classes.append(class_name)

        subclasses_mapping = class_mapping.get("subclasses")

        if "." in code:
            code = code.split(".")[0]

        if code[1:].isnumeric():
            code = code[0]

        if len(code) > 2:
            code = code[:2]

        for subclass_mapping in subclasses_mapping:
            subclass_name = subclass_mapping.get("name")
            if subclass_mapping.get("code") == code:
                subclasses.append(subclass_name)
                break

    return {
        "classes": json.dumps(classes),
        "subclasses": json.dumps(subclasses),
    }


def write_book_to_file(record: Record, output: Path):
    """
    Processes a MARC record and appends the extracted book data to a CSV file.

    Args:
        record: The MARC record being processed.
    """
    id = record.get_fields("001")[0].value()

    title = record.title
    pub_year = record.pubyear
    summary = "\n".join(get_fields_value(record.get_fields("520")))
    notes = "\n".join(
        get_fields_value(
            record.get_fields(
                "500",
                "505",
                "508",
                "534",
                "546",
            )
        )
    )
    language_code = ",".join(get_fields_value(record.get_fields("041")))
    language_code = language_code if language_code else None
    subclasses_code = get_fields_value(record.get_fields("050"))
    subclasses_code = subclasses_code[0].split(" ") if subclasses_code else []

    authors = get_book_authors(record)
    publisher = get_book_publisher(record)
    subjects = get_book_subjects(record)
    serie = get_book_serie(record)
    subclasses = get_book_subclasses(subclasses_code, class_mapping)

    book = {
        "id": id,
        "title": title,
        "pub_year": pub_year,
        "summary": summary,
        "notes": notes,
        "language_code": language_code,
    }
    book = book | authors | publisher | subjects | serie | subclasses

    df = pd.DataFrame([book])

    df.to_csv(output, mode="a", index=False, header=False)
    typer.echo(f"Processed book: {id}")


@app.command()
def process_data(
    output: Path = typer.Option(
        ..., "--output", "-o", help="Path to the output file (CSV)"
    ),
    source: Path = typer.Argument(
        help="Path to the source file (MarcXML)",
        exists=True,
        file_okay=True,
        readable=True,
    ),
):
    """Preprocess books data from a MarcXML source file to a CSV dataset."""
    typer.echo("Starting preprocessing...")
    with open(output, "w") as f:
        f.write("")
    map_xml(lambda x: write_book_to_file(x, output), source)

    typer.echo("Adding columns...")
    df = pd.read_csv(output, header=None)
    df.columns = [
        "id",
        "title",
        "pub_year",
        "summary",
        "notes",
        "language_code",
        "authors",
        "publisher",
        "subjects",
        "serie",
        "classes",
        "subclasses",
    ]

    df.to_csv(output, index=False)
    typer.echo("Preprocessing finished successfully!")


if __name__ == "__main__":
    app()
