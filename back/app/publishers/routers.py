from typing import Annotated

from fastapi import APIRouter, Query

from app.books.models import BookRead
from app.config.db import SessionDep
from app.publishers.models import PublisherCreate, PublisherRead
from app.publishers.services import (
    add_publisher,
    get_books_by_publisher,
    get_publisher,
    get_publishers,
)

router = APIRouter(prefix="/publishers", tags=["Publishers"])


@router.post("", response_model=PublisherRead)
def create_publisher(publisher: PublisherCreate, session: SessionDep):
    return add_publisher(publisher, session)


@router.get("", response_model=list[PublisherRead])
def read_publishers(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 10,
):
    return get_publishers(offset, limit, session)


@router.get("/{id}", response_model=PublisherRead)
def read_publisher(id: int, session: SessionDep):
    return get_publisher(id, session)


@router.get("/{id}/books", response_model=list[BookRead])
def read_books_by_publisher(
    id: int,
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 10,
):
    return get_books_by_publisher(id, offset, limit, session)
