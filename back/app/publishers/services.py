from typing import Annotated

from fastapi import HTTPException, Query
from sqlmodel import Session, select

from app.publishers.models import Publisher, PublisherCreate


def add_publisher(publisher: PublisherCreate, session: Session):
    db_publisher = Publisher.model_validate(publisher)
    session.add(db_publisher)
    session.commit()
    session.refresh(db_publisher)
    return db_publisher


def get_publishers(offset: int, limit: Annotated[int, Query], session: Session):
    publishers = session.exec(
        select(Publisher).offset(offset).limit(limit)
    ).all()
    return publishers


def get_publisher(publisher_id: int, session: Session):
    publisher = session.get(Publisher, publisher_id)
    if not publisher:
        raise HTTPException(status_code=404, detail="Publisher not found")
    return publisher
