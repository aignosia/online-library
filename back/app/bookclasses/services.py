import math

from fastapi import HTTPException
from sqlmodel import Session, func, select

from app.bookclasses.models import BookClass, BookClassCreate
from app.books.models import Book, BookRead
from app.links.models import BookSubclassLink
from app.subclasses.models import Subclass


def add_class(book_class: BookClassCreate, session: Session):
    db_class = BookClass.model_validate(book_class)
    session.add(db_class)
    session.commit()
    session.refresh(db_class)
    return db_class


def get_classes(offset: int | None, limit: int | None, session: Session):
    if not limit:
        bookclasses = list(
            session.exec(select(BookClass).offset(offset).limit(limit)).all()
        )
    else:
        bookclasses = list(session.exec(select(BookClass)).all())
    return bookclasses


def get_class(id: int, session: Session):
    book_class = session.get(BookClass, id)
    if not book_class:
        raise HTTPException(status_code=404, detail="Class not found")
    return book_class


def get_books_by_class(id: int, offset: int, limit: int, session: Session):
    books = session.exec(
        select(Book)
        .join(BookSubclassLink)
        .join(Subclass)
        .join(BookClass)
        .where(BookClass.id == id)
        .order_by(Book.id)  # ty:ignore[invalid-argument-type]
        .offset(offset)
        .limit(limit)
    ).all()
    books = [BookRead.model_validate(book) for book in books]
    book_count = (
        session.exec(
            select(func.count())
            .select_from(Book)
            .join(BookSubclassLink)
            .join(Subclass)
            .join(BookClass)
            .where(BookClass.id == id)
        ).one_or_none()
        or 0
    )
    max_offset = max(math.ceil(float(book_count / limit)) - 1, 0)
    return {"total_books": book_count, "max_offset": max_offset, "books": books}
