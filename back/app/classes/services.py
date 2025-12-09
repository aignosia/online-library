from fastapi import HTTPException
from sqlmodel import Session, select

from app.classes.models import Class, ClassCreate


def add_class(_class: ClassCreate, session: Session):
    db_class = Class.model_validate(_class)
    session.add(db_class)
    session.commit()
    session.refresh(db_class)
    return db_class


def get_classes(limit: int, offset: int, session: Session):
    classes = session.exec(select(Class).limit(limit).offset(offset)).all()
    return classes


def get_class(id: int, session: Session):
    _class = session.get(Class, id)
    if not _class:
        raise HTTPException(status_code=404, detail="Class not found")
    return _class
