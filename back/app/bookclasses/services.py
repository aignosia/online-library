from fastapi import HTTPException
from sqlmodel import Session, select

from app.bookclasses.models import BookClass, BookClassCreate


def add_class(book_class: BookClassCreate, session: Session):
    db_class = BookClass.model_validate(book_class)
    session.add(db_class)
    session.commit()
    session.refresh(db_class)
    return db_class


def get_classes(offset: int, limit: int | None, session: Session):
    if not limit:
        bookclasses = session.exec(
            select(BookClass).offset(offset).limit(limit)
        ).all()
    else:
        bookclasses = session.exec(select(BookClass)).all()
    return bookclasses


def get_class(id: int, session: Session):
    book_class = session.get(BookClass, id)
    if not book_class:
        raise HTTPException(status_code=404, detail="Class not found")
    return book_class
