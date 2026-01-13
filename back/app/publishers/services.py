from fastapi import HTTPException
from sqlmodel import Session, select

from app.books.models import Book
from app.publishers.models import Publisher, PublisherCreate


def add_publisher(publisher: PublisherCreate, session: Session):
    db_publisher = Publisher.model_validate(publisher)
    session.add(db_publisher)
    session.commit()
    session.refresh(db_publisher)
    return db_publisher


def get_publishers(offset: int, limit: int, session: Session):
    publishers = session.exec(
        select(Publisher).offset(offset).limit(limit)
    ).all()
    return publishers


def get_publisher(id: int, session: Session):
    publisher = session.get(Publisher, id)
    if not publisher:
        raise HTTPException(status_code=404, detail="Publisher not found")
    return publisher


def get_books_by_publisher(id: int, offset: int, limit: int, session: Session):
    books = session.exec(
        select(Book)
        .join(Publisher)
        .where(Publisher.id == id)
        .order_by(Book.id)  # ty:ignore[invalid-argument-type]
        .offset(offset)
        .limit(limit)
    ).all()
    return books
