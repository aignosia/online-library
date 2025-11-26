from fastapi import APIRouter

from app.config.db import SessionDep
from app.subjects.models import SubjectCreate, SubjectRead
from app.subjects.services import add_subject, get_subject, get_subjects

router = APIRouter(prefix="/subjects", tags=["Subjects"])


@router.post("", response_model=SubjectRead)
def create_subject(subject: SubjectCreate, session: SessionDep):
    return add_subject(subject, session)


@router.get("", response_model=list[SubjectRead])
def read_subjects(session: SessionDep, offset: int, limit: int):
    return get_subjects(offset, limit, session)


@router.get("/{id}", response_model=SubjectRead)
def read_subject(id: int, session: SessionDep):
    return get_subject(id, session)
