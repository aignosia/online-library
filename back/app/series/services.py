from fastapi import HTTPException
from sqlmodel import Session, select

from app.books.models import Book
from app.series.models import Serie, SerieCreate


def add_serie(serie: SerieCreate, session: Session):
    db_serie = Serie.model_validate(serie)
    session.add(db_serie)
    session.commit()
    session.refresh(db_serie)
    return db_serie


def get_series(offset: int | None, limit: int | None, session: Session):
    series = session.exec(select(Serie).offset(offset).limit(limit)).all()
    return series


def get_serie(id: int, session: Session):
    serie = session.get(Serie, id)
    if not serie:
        raise HTTPException(status_code=404, detail="Serie not found")
    return serie


def get_books_by_serie(id: int, offset: int, limit: int, session: Session):
    books = session.exec(
        select(Book)
        .join(Serie)
        .where(Serie.id == id)
        .offset(offset)
        .limit(limit)
    ).all()
    return books
