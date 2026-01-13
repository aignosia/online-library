from typing import Annotated

from fastapi import APIRouter, Query

from app.books.models import BookRead
from app.config.db import SessionDep
from app.subjects.models import SubjectCreate, SubjectRead
from app.subjects.services import (
    add_subject,
    get_books_by_subject,
    get_subject,
    get_subjects,
)

router = APIRouter(prefix="/subjects", tags=["Subjects"])


@router.post("", response_model=SubjectRead)
def create_subject(subject: SubjectCreate, session: SessionDep):
    return add_subject(subject, session)


@router.get("", response_model=list[SubjectRead])
def read_subjects(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 10,
):
    return get_subjects(offset, limit, session)


@router.get("/{id}", response_model=SubjectRead)
def read_subject(id: int, session: SessionDep):
    return get_subject(id, session)


@router.get("/{id}/books", response_model=list[BookRead])
def read_books_by_subject(
    id: int,
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    return get_books_by_subject(id, offset, limit, session)
