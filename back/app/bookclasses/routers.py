from typing import Annotated

from fastapi import APIRouter, Query

from app.bookclasses.models import (
    BookClassCreate,
    BookClassRead,
    BookClassReadWithSubclasses,
)
from app.bookclasses.services import (
    add_class,
    get_books_by_class,
    get_class,
    get_classes,
)
from app.books.models import BookRead
from app.config.db import SessionDep

router = APIRouter(prefix="/classes", tags=["Classes"])


@router.post("", response_model=BookClassRead)
def create_class(book_class: BookClassCreate, session: SessionDep):
    return add_class(book_class, session)


@router.get("", response_model=list[BookClassReadWithSubclasses])
def read_classes(
    session: SessionDep,
    offset: int | None = None,
    limit: Annotated[int | None, Query(le=100)] = None,
):
    return get_classes(offset, limit, session)


@router.get("/{id}", response_model=BookClassReadWithSubclasses)
def read_class(id: int, session: SessionDep):
    return get_class(id, session)


@router.get("/{id}/books")
def read_books_by_class(
    id: int,
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(gt=0, le=100)] = 10,
):
    return get_books_by_class(id, offset, limit, session)
