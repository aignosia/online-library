from fastapi import HTTPException
from sqlmodel import Session, select

from app.books.models import Book
from app.links.models import BookSubclassLink
from app.subclasses.models import Subclass, SubclassCreate


def add_subclass(subclass: SubclassCreate, session: Session):
    db_subclass = Subclass.model_validate(subclass)
    session.add(db_subclass)
    session.commit()
    session.refresh(db_subclass)
    return db_subclass


def get_subclasses(offset: int | None, limit: int | None, session: Session):
    subclasses = session.exec(
        select(Subclass).offset(offset).limit(limit)
    ).all()
    return subclasses


def get_subclass(id: int, session: Session):
    subclass = session.get(Subclass, id)
    if not subclass:
        raise HTTPException(status_code=404, detail="Subclass not found")
    return subclass


def get_books_by_subclass(id: int, offset: int, limit: int, session: Session):
    books = session.exec(
        select(Book)
        .join(BookSubclassLink)
        .join(Subclass)
        .where(Subclass.id == id)
        .offset(offset)
        .limit(limit)
    ).all()
    return books
