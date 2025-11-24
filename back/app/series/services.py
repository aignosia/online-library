from fastapi import HTTPException
from sqlmodel import Session, select

from app.series.models import Serie, SerieCreate


def add_serie(serie: SerieCreate, session: Session):
    db_serie = Serie.model_validate(serie)
    session.add(db_serie)
    session.commit()
    session.refresh(db_serie)
    return db_serie


def get_series(offset: int, limit: int, session: Session):
    series = session.exec(select().offset(offset).limit(limit)).all()
    return series


def get_serie(id: int, session: Session):
    serie = session.get(Serie, id)
    if not serie:
        raise HTTPException(status_code=404, detail="Serie not found")
    return serie
