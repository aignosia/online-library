from typing import Annotated

from fastapi import HTTPException, Query
from sqlmodel import Session, select

from app.books.models import Book, BookCreate


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
