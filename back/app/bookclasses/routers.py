from fastapi import APIRouter

from app.bookclasses.models import (
    BookClassCreate,
    BookClassRead,
    BookClassReadWithSubclasses,
)
from app.bookclasses.services import add_class, get_class, get_classes
from app.config.db import SessionDep

router = APIRouter(prefix="/classes", tags=["Classes"])


@router.post("", response_model=BookClassRead)
def create_class(book_class: BookClassCreate, session: SessionDep):
    return add_class(book_class, session)


@router.get("", response_model=list[BookClassReadWithSubclasses])
def read_classes(
    session: SessionDep, offset: int = 0, limit: int | None = None
):
    return get_classes(offset, limit, session)


@router.get("/{id}", response_model=BookClassReadWithSubclasses)
def read_class(id: int, session: SessionDep):
    return get_class(id, session)
