from typing import Annotated

from fastapi import APIRouter, Query

from app.books.models import BookRead
from app.config.db import SessionDep
from app.subclasses.models import (
    SubclassCreate,
    SubclassRead,
)
from app.subclasses.services import (
    add_subclass,
    get_books_by_subclass,
    get_subclass,
    get_subclasses,
)

router = APIRouter(prefix="/subclasses", tags=["Subclasses"])


@router.post("", response_model=SubclassRead)
def create_subclass(subclass: SubclassCreate, session: SessionDep):
    return add_subclass(subclass, session)


@router.get("", response_model=list[SubclassRead])
def read_subclasses(
    session: SessionDep,
    offset: int | None = None,
    limit: Annotated[int | None, Query(le=100)] = None,
):
    return get_subclasses(offset, limit, session)


@router.get("/{id}", response_model=SubclassRead)
def read_subclass(id: int, session: SessionDep):
    return get_subclass(id, session)


@router.get("/{id}/books", response_model=list[BookRead])
def read_books_by_subclass(
    id: int,
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 10,
):
    return get_books_by_subclass(id, offset, limit, session)
