from sqlmodel import Session, select

from app.subjects.models import Subject, SubjectCreate


def add_subject(subject: SubjectCreate, session: Session):
    db_subject = Subject.model_validate(subject)
    session.add(db_subject)
    session.commit()
    session.refresh(db_subject)
    return db_subject


def get_subjects(offset: int, limit: int, session: Session):
    subjects = session.exec(select(Subject).offset(offset).limit(limit)).all()
    return subjects


def get_subject(id: int, session: Session):
    subject = session.get(Subject, id)
    if not subject:
        raise Exception(status_code=404, details="Subject not found")
    return subject
