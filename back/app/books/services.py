from fastapi import HTTPException
from sqlmodel import Session, func, or_, select

from app.authors.models import Author
from app.books.models import Book, BookCreate
from app.links.models import BookAuthorLink


def add_book(book: BookCreate, session: Session):
    db_book = Book.model_validate(book)
    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return db_book


def get_books(offset: int, limit: int, session: Session):
    books = session.exec(select(Book).offset(offset).limit(limit)).all()
    return books


def get_book(book_id: int, session: Session):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


def get_books_search(q: str, session: Session):
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
        .distinct()
    ).all()

    return results


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
