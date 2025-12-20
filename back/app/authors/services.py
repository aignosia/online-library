from fastapi import HTTPException
from sqlmodel import Session, select

from app.authors.models import Author, AuthorCreate
from app.books.models import Book
from app.links.models import BookAuthorLink


def add_author(author: AuthorCreate, session: Session):
    db_author = Author.model_validate(author)
    session.add(db_author)
    session.commit()
    session.refresh(db_author)
    return db_author


def get_authors(offset: int, limit: int, session: Session):
    authors = session.exec(select(Author).offset(offset).limit(limit)).all()
    return authors


def get_author(id: int, session: Session):
    author = session.get(Author, id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


def get_books_by_author(id: int, offset: int, limit: int, session: Session):
    books = session.exec(
        select(Book)
        .join(BookAuthorLink)
        .join(Author)
        .where(Author.id == id)
        .order_by(Book.id)  # ty:ignore[invalid-argument-type]
        .offset(offset)
        .limit(limit)
    ).all()

    return books
