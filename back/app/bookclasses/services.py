from fastapi import HTTPException
from sqlmodel import Session, select

from app.bookclasses.models import BookClass, BookClassCreate
from app.books.models import Book
from app.links.models import BookSubclassLink
from app.subclasses.models import Subclass


def add_class(book_class: BookClassCreate, session: Session) -> BookClass:
    db_class = BookClass.model_validate(book_class)
    session.add(db_class)
    session.commit()
    session.refresh(db_class)
    return db_class


def get_classes(
    offset: int | None, limit: int | None, session: Session
) -> list[BookClass]:
    if not limit:
        bookclasses = session.exec(
            select(BookClass).offset(offset).limit(limit)
        ).all()
    else:
        bookclasses = session.exec(select(BookClass)).all()
    return bookclasses


def get_class(id: int, session: Session) -> BookClass:
    book_class = session.get(BookClass, id)
    if not book_class:
        raise HTTPException(status_code=404, detail="Class not found")
    return book_class


def get_books_by_class(
    id: int, offset: int, limit: int, session: Session
) -> list[Book]:
    books = session.exec(
        select(Book)
        .join(BookSubclassLink)
        .join(Subclass)
        .join(BookClass)
        .where(BookClass.id == id)
        .order_by(Book.id)
        .offset(offset)
        .limit(limit)
    ).all()
    return books
