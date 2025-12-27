import json
import re
from typing import Any

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
session = Session(engine)


class Cache:
    def __init__(self):
        self.books: dict[str, Book] = {}
        self.authors: dict[str, Author] = {}
        self.publishers: dict[str, Publisher] = {}
        self.subjects: dict[str, Subject] = {}
        self.series: dict[str, Serie] = {}
        self.subclasses: dict[str, Subclass] = {}
        self.bookclasses: dict[str, BookClass] = {}


cache = Cache()


with open("app/seeds/loc_classification.json", "r") as f:
    class_mapping = json.load(f)


def get_fields_value(fields_list: list[Field]) -> list[str]:
    return list(map(lambda x: x.value(), fields_list))


def get_book_authors(record: Record) -> list[Author]:
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
    publisher_name = re.sub(r"[^a-zA-ZÀ-ÿ\s\-]", "", record.publisher)
    if not publisher_name:
        return None

    if not cache.publishers.get(publisher_name):
        cache.publishers[publisher_name] = Publisher(name=publisher_name)

    return cache.publishers[publisher_name]


def get_book_subjects(record: Record) -> list[Subject]:
    subject_names = get_fields_value(record.get_fields("653"))
    subjects = []
    for subject_name in subject_names:
        if not cache.subjects.get(subject_name):
            cache.subjects[subject_name] = Subject(name=subject_name)

        subjects.append(cache.subjects[subject_name])

    return subjects


def get_book_serie(record: Record) -> Serie | None:
    serie_field = next(iter(record.get_fields("490")), None)
    if not serie_field:
        return None

    serie_name = serie_field.value()
    if not cache.series.get(serie_name):
        cache.series[serie_name] = Serie(name=serie_name)

    return cache.series[serie_name]


def get_book_subclasses(codes: list[str], mapping: Any) -> list[Subclass]:
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


def get_book_files_locations(url: str) -> list[File]:
    id = next(iter(url.rsplit("/")))
    locations = [
        File(type="epub3_images", location=f"{url}.epub3.images"),
        File(type="epub_images", location=f"{url}.epub.images"),
        File(type="epub_noimages", location=f"{url}.epub.noimages"),
        File(type="kindle", location=f"{url}.kf8.images"),
        File(type="kindle_legacy", location=f"{url}.kindle.images"),
        File(type="txt_utf8", location=f"{url}.txt.utf8"),
        File(type="html_zip", location=f"{url}/pg{id}-h.zip"),
    ]
    return locations


def insert_book_in_db(record: Record):
    id = record.get_fields("001")[0].value()

    title = record.title
    pub_year = record.pubyear
    isbn = record.isbn
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
    locations_url = next(iter(get_fields_value(record.get_fields("856"))))
    cover = f"https://www.gutenberg.org/cache/epub/{id}/pg{id}.cover.medium.jpg"

    authors = get_book_authors(record)
    publisher = get_book_publisher(record)
    subjects = get_book_subjects(record)
    serie = get_book_serie(record)
    locations = get_book_files_locations(locations_url)
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

    print(f"Processed book: {id}")


def seed_database():
    print("Seeding start")
    map_xml(insert_book_in_db, "downloads/pgmarc.xml")
    print("Adding entries...")
    session.add_all(cache.books.values())
    print("Commiting entries...")
    session.commit()

    print("Seeding complete")


if __name__ == "__main__":
    seed_database()
