import json
import re
from typing import Any

import typer
from pymarc import Field, Record, map_xml
from sqlmodel import Session

from app import model_registry  # noqa: F401
from app.authors.models import Author
from app.bookclasses.models import BookClass
from app.books.models import Book
from app.config.db import engine, init_db
from app.files.models import File
from app.publishers.models import Publisher
from app.series.models import Serie
from app.subclasses.models import Subclass
from app.subjects.models import Subject

init_db()


class Cache:
    """
    Temporary caching system to store entities created during the process.

    Allows reusing existing instances of authors, publishers, etc., to avoid
    unique constraint violations and reduce redundant queries before the
    final commit.
    """

    def __init__(self):
        """Initialize cache dictionaries for each entity type."""
        self.books: dict[str, Book] = {}
        self.authors: dict[str, Author] = {}
        self.publishers: dict[str, Publisher] = {}
        self.subjects: dict[str, Subject] = {}
        self.series: dict[str, Serie] = {}
        self.subclasses: dict[str, Subclass] = {}
        self.bookclasses: dict[str, BookClass] = {}


cache = Cache()


with open("scripts/loc_classification.json", "r") as f:
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


def get_book_authors(record: Record) -> list[Author]:
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
        fuller_name_sf = author.get_subfields("q")
        fuller_name = (
            re.sub(
                r"[^a-zA-ZÀ-ÿ\s\-]",
                "",
                fuller_name_sf[0],
            )
            if fuller_name_sf
            else None
        )

        if not firstname and not lastname:
            continue

        key_name = f"{firstname}_{lastname}"
        if not cache.authors.get(key_name):
            cache.authors[key_name] = Author(
                firstname=firstname,
                lastname=lastname,
                birth_year=birth_year,
                death_year=death_year,
                fuller_name=fuller_name,
            )
        if cache.authors[key_name] not in authors:
            authors.append(cache.authors[key_name])

    return authors


def get_book_publisher(record: Record) -> Publisher | None:
    """
    Extracts the publisher from a MARC record.

    Args:
        record: The MARC record.

    Returns:
        A Publisher object or None if no information is found.
    """
    publisher_name = re.sub(r"[^a-zA-ZÀ-ÿ\s\-]", "", record.publisher)
    if not publisher_name:
        return None

    if not cache.publishers.get(publisher_name):
        cache.publishers[publisher_name] = Publisher(name=publisher_name)

    return cache.publishers[publisher_name]


def get_book_subjects(record: Record) -> list[Subject]:
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
        if not cache.subjects.get(subject_name):
            cache.subjects[subject_name] = Subject(name=subject_name)

        subjects.append(cache.subjects[subject_name])

    return subjects


def get_book_serie(record: Record) -> Serie | None:
    """
    Extracts the collection/series from a MARC record via tag 490.

    Args:
        record: The MARC record.

    Returns:
        A Serie object or None.
    """
    serie_field = next(iter(record.get_fields("490")), None)
    if not serie_field:
        return None

    serie_name = serie_field.value()
    if not cache.series.get(serie_name):
        cache.series[serie_name] = Serie(name=serie_name)

    return cache.series[serie_name]


def get_book_subclasses(codes: list[str], mapping: Any) -> list[Subclass]:
    """
    Maps classification codes (LOC) to Subclass objects.

    Args:
        codes: List of extracted classification codes (tag 050).
        mapping: Mapping dictionary loaded from JSON.

    Returns:
        A list of Subclass objects associated with their respective BookClass.
    """
    subclasses = []
    for code in codes:
        bookclass_mapping = next(
            filter(lambda x: x.get("code") == code[0], mapping), None
        )
        if not bookclass_mapping:
            continue

        bookclass_name = bookclass_mapping.get("name")
        if not cache.bookclasses.get(bookclass_name):
            cache.bookclasses[bookclass_name] = BookClass(name=bookclass_name)

        subclasses_mapping = bookclass_mapping.get("subclasses")

        if "." in code:
            code = code.split(".")[0]

        if code[1:].isnumeric():
            code = code[0]

        if len(code) > 2:
            code = code[:-1]

        for subclass_mapping in subclasses_mapping:
            subclass_name = subclass_mapping.get("name")
            if subclass_mapping.get("code") == code:
                if not cache.subclasses.get(subclass_name):
                    cache.subclasses[subclass_name] = Subclass(
                        name=subclass_name,
                        bookclass=cache.bookclasses[bookclass_name],
                    )
                subclasses.append(cache.subclasses[subclass_name])
                break

    return subclasses


def get_book_files_locations(url: str, book_id: int) -> list[File]:
    """
    Generates the list of available files (EPUB, Kindle, TXT) for a book.

    Based on Project Gutenberg's standard storage structure.

    Args:
        url: The base resource URL.

    Returns:
        A list of File objects with their types and locations.
    """
    root_url = f"{url}/{book_id}/pg{book_id}"
    file_types = {
        "epub3_images": {
            "type": "epub3_images",
            "label": "EPUB3 (E-readers incl. Send-to-Kindle)",
            "url_ext": "-images-3.epub",
        },
        "epub_images": {
            "type": "epub_images",
            "label": "EPUB3 (E-readers Incl. Send-to-Kindle)",
            "url_ext": "-images.epub",
        },
        "epub_noimages": {
            "type": "epub_noimages",
            "label": "EPUB (No Images, Older E-readers)",
            "url_ext": ".epub",
        },
        "kindle": {
            "type": "kindle",
            "label": "Kindle",
            "url_ext": "-images-kf8.mobi",
        },
        "kindle_legacy": {
            "type": "kindle_legacy",
            "label": "Older Kindles",
            "url_ext": "-images.mobi",
        },
        "txt_utf8": {
            "type": "txt_utf8",
            "label": "Plain Text UTF-8",
            "url_ext": ".txt",
        },
        "html_zip": {
            "type": "html_zip",
            "label": "HTML (Zip)",
            "url_ext": "-h.zip",
        },
    }
    locations = [
        File(
            type=file_types[file_type]["type"],
            label=file_types[file_type]["label"],
            location=f"{root_url}{file_types[file_type]['url_ext']}",
        )
        for file_type in file_types.keys()
    ]
    return locations


def insert_book_in_db(record: Record):
    """
    Transforms a MARC record into a Book object and adds it to the cache.

    This function is called by `map_xml` for each record found.
    It extracts title, ISBN, summary, notes, language, and calls
    auxiliary extraction functions.

    Args:
        record: The MARC record being processed.
    """
    id = record.get_fields("001")[0].value()

    title = record.title
    pub_year = record.pubyear
    isbn = record.isbn
    summary = "\n".join(get_fields_value(record.get_fields("520")))
    notes = get_fields_value(
        record.get_fields(
            "500",
            "505",
            "508",
            "534",
            "546",
        )
    )
    language_code = ",".join(get_fields_value(record.get_fields("041")))
    language_code = language_code if language_code else None
    subclasses_code = get_fields_value(record.get_fields("050"))
    location_url = "https://www.gutenberg.org/cache/epub"
    cover = f"https://www.gutenberg.org/cache/epub/{id}/pg{id}.cover.medium.jpg"

    authors = get_book_authors(record)
    publisher = get_book_publisher(record)
    subjects = get_book_subjects(record)
    serie = get_book_serie(record)
    locations = get_book_files_locations(location_url, id)
    subclasses = get_book_subclasses(subclasses_code, class_mapping)

    book = Book(
        id=id,
        title=title,
        pub_year=pub_year,
        isbn=isbn,
        summary=summary,
        notes=notes,
        language_code=language_code,
        authors=authors,
        publisher=publisher,
        subjects=subjects,
        serie=serie,
        subclasses=subclasses,
        files=locations,
        cover=cover,
    )

    cache.books[id] = book

    typer.echo(f"Processed books: {len(cache.books)}\r", nl=False)


def seed_books(data: str):
    """
    Main entry point for database seeding.

    Reads the XML file, processes records, adds objects to the session,
    and performs the final commit.
    """
    with Session(engine) as session:
        if session.get(Book, 1):
            typer.echo("Book seeding skipped: book table not empty")
            return

        map_xml(insert_book_in_db, data)
        typer.echo(f"Treated books: {len(cache.books)}")
        typer.echo("Adding entries...")
        session.add_all(cache.books.values())
        typer.echo("Commiting entries...")
        session.commit()
