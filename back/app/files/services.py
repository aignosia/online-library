from fastapi import HTTPException
from sqlmodel import Session, select

from app.files.models import File, FileCreate


def add_file(file: FileCreate, session: Session):
    db_file = File.model_validate(file)
    session.add(db_file)
    session.commit()
    session.refresh(db_file)
    return db_file


def get_files(offset: int, limit: int, session: Session):
    files = session.exec(select(File).offset(offset).limit(limit)).all()
    return files


def get_file(id: int, session: Session):
    file = session.get(File, id)
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    return file
