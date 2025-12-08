from fastapi import HTTPException
from sqlmodel import Session, select

from app.subclasses.models import Subclass, SubclassCreate


def add_subclass(subclass: SubclassCreate, session: Session):
    db_subclass = Subclass.model_validate(subclass)
    session.add(db_subclass)
    session.commit()
    session.refresh(db_subclass)
    return db_subclass


def get_subclasses(limit: int, offset: int, session: Session):
    subclasses = session.exec(
        select(Subclass).limit(limit).offset(offset)
    ).all()
    return subclasses


def get_subclass(id: int, session: Session):
    subclass = session.get(Subclass, id)
    if not subclass:
        raise HTTPException("Subclass not found")
    return subclass
