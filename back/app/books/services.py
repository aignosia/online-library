import logging
import math
import re

import fugashi
import jieba
import tltk
from fastapi import HTTPException
from konlpy.tag import Kkma
from sqlmodel import Session, func, or_, select
from stop_words import safe_get_stop_words
from underthesea import word_tokenize

from app.authors.models import Author
from app.books.models import Book, BookCreate, BookRead
from app.links.models import BookAuthorLink, UserBookDownload
from app.recmodel.services import compute_embedding

logging.getLogger().setLevel(logging.CRITICAL)


def filter_stop_words(lang: str, text: str):
    stop_words = set(safe_get_stop_words(lang))
    words = text.split()
    filtered = [w for w in words if w not in stop_words]
    return " ".join(filtered)


def get_book_tfidf_text(book: Book) -> str:
    authors_str = " | ".join(
        f"{a.firstname + '_' if a.firstname else ''}{a.lastname}"
        for a in book.authors
    )
    subjects_str = " | ".join([s.name for s in book.subjects] * 2)
    bookclasses_str = " | ".join(
        [s.bookclass.name for s in book.subclasses] * 2
    )
    subclasses_str = " | ".join([s.name for s in book.subclasses] * 2)
    text = " | ".join(
        [
            authors_str,
            book.title,
            bookclasses_str,
            subclasses_str,
            subjects_str,
        ]
    )
    text = re.sub(r"[^a-zA-Z0-9_|\-\s]", "", text.lower())
    text = re.sub(r"\s+", " ", text).strip()
    text = filter_stop_words(
        book.language_code[:2] if book.language_code else "en", text
    )
    lc = book.language_code[:2] if book.language_code else "en"
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


def add_book(book: BookCreate, session: Session):
    db_book = Book.model_validate(book)
    book_tfidf_text = get_book_tfidf_text(db_book)
    book.embedding = compute_embedding(book_tfidf_text)
    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return db_book


def get_books(offset: int, limit: int, session: Session):
    book_count = get_book_count(session)
    books = session.exec(select(Book).offset(offset).limit(limit)).all()
    max_offset = math.ceil(float(book_count / limit)) - 1
    return {
        "total_books": book_count,
        "max_offset": max_offset,
        "books": books,
    }


def get_book(id: int, session: Session):
    book = session.get(Book, id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    return book


def get_books_search(q: str, offset: int, limit: int, session: Session):
    query_term = " & ".join(f"{word}" for word in q.split())
    ts_query = func.to_tsquery("simple", query_term)

    book_vector = func.to_tsvector("simple", func.coalesce(Book.title, ""))
    author_vector = func.to_tsvector(
        "simple",
        func.coalesce(Author.firstname, "")
        + " "
        + func.coalesce(Author.lastname),
    )

    results = session.exec(
        select(Book)
        .outerjoin(BookAuthorLink)
        .outerjoin(Author)
        .where(
            or_(
                book_vector.op("@@")(ts_query),
                author_vector.op("@@")(ts_query),
            )
        )
        .group_by(Book.id)  # ty:ignore[invalid-argument-type]
        .offset(offset)
        .limit(limit)
    ).all()
    results = [BookRead.model_validate(book) for book in results]
    result_count = (
        session.exec(
            select(func.count())
            .select_from(Book)
            .outerjoin(BookAuthorLink)
            .outerjoin(Author)
            .where(
                or_(
                    book_vector.op("@@")(ts_query),
                    author_vector.op("@@")(ts_query),
                )
            )
        ).one_or_none()
        or 0
    )
    max_offset = math.ceil(float(result_count / limit)) - 1

    return {
        "total_books": result_count,
        "max_offset": max_offset,
        "books": results,
    }


def get_search_autocomplete(q: str, session: Session):
    query_term = " & ".join(f"{word}:*" for word in q.split())
    ts_query = func.to_tsquery("simple", query_term)

    book_tsvector = func.to_tsvector("simple", func.coalesce(Book.title, ""))
    author_tsvector = func.to_tsvector(
        "simple",
        func.coalesce(Author.firstname, "")
        + " "
        + func.coalesce(Author.lastname, ""),
    )

    results = list(
        session.exec(
            select(Book.title).where(book_tsvector.op("@@")(ts_query))
        ).all()
    ) + list(
        " ".join(e for e in it if e is not None)
        for it in session.exec(
            select(Author.firstname, Author.lastname).where(
                author_tsvector.op("@@")(ts_query)
            )
        ).all()
    )

    return list(dict.fromkeys(results[:10]))


def get_book_count(session: Session):
    count = session.exec(select(func.count()).select_from(Book)).one()
    return count


def get_popular_books(offset: int, limit: int, session: Session):
    subquery = (
        select(
            UserBookDownload.book_id,
            func.count(UserBookDownload.book_id).label("download"),
        )
        .group_by(UserBookDownload.book_id)
        .offset(offset)
        .limit(limit)
        .subquery()
    )
    books = session.exec(
        select(Book)
        .outerjoin(subquery)
        .order_by(
            func.coalesce(subquery.c.download, 0).label("download").desc()
        )
        .offset(offset)
        .limit(limit)
    ).all()
    books = [BookRead.model_validate(book) for book in books]
    max_offset = math.ceil(float(100 / limit)) - 1
    if offset > max_offset:
        books = []
    return {
        "total_books": 100,
        "max_offset": max_offset,
        "books": books,
    }


def rerank_books(query: Book, response: list[Book], limit: int):
    reranked_response = response.copy()
    reranked_response.sort(
        key=lambda x: x.language_code == query.language_code, reverse=True
    )
    if query in response:
        reranked_response.remove(query)
    return reranked_response[:limit]


def get_similar_books(id: int, offset: int, limit: int, session: Session):
    book = session.get(Book, id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    similar_books = session.exec(
        select(Book)
        .where(Book.id != book.id)
        .order_by(Book.embedding.cosine_distance(book.embedding))  # ty:ignore[possibly-missing-attribute]
        .limit(limit + 50)
    ).all()
    similar_books = [
        BookRead.model_validate(book)
        for book in rerank_books(book, list(similar_books), limit)
    ]
    max_offset = math.ceil(float(100 / limit)) - 1
    if offset > max_offset:
        similar_books = []
    return {
        "total_books": 100,
        "max_offset": max_offset,
        "books": similar_books,
    }
