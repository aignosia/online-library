from typing import Annotated

from fastapi import APIRouter, Query

from app.authors.models import AuthorCreate, AuthorRead
from app.authors.services import (
    add_author,
    get_author,
    get_authors,
    get_books_by_author,
)
from app.books.models import BookRead
from app.config.db import SessionDep

router = APIRouter(prefix="/authors", tags=["Authors"])


@router.post("", response_model=AuthorRead)
def create_author(author: AuthorCreate, session: SessionDep):
    return add_author(author, session)


@router.get("", response_model=list[AuthorRead])
def read_authors(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(gt=0, le=100)] = 10,
):
    return get_authors(offset, limit, session)


@router.get("/{id}", response_model=AuthorRead)
def read_author(id: int, session: SessionDep):
    return get_author(id, session)


@router.get("/{id}/books", response_model=list[BookRead])
def read_books_by_author(
    id: int,
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(gt=0, le=100)] = 10,
):
    return get_books_by_author(id, offset, limit, session)
