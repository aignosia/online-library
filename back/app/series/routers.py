from typing import Annotated

from fastapi import APIRouter, Query

from app.books.models import BookRead
from app.config.db import SessionDep
from app.series.models import SerieCreate, SerieRead
from app.series.services import (
    add_serie,
    get_books_by_serie,
    get_serie,
    get_series,
)

router = APIRouter(prefix="/series", tags=["Series"])


@router.post("", response_model=SerieRead)
def create_serie(serie: SerieCreate, session: SessionDep):
    return add_serie(serie, session)


@router.get("", response_model=list[SerieRead])
def read_series(
    session: SessionDep,
    offset: int | None = None,
    limit: Annotated[int | None, Query(le=100)] = None,
):
    return get_series(offset, limit, session)


@router.get("/{id}", response_model=SerieRead)
def read_serie(id: int, session: SessionDep):
    return get_serie(id, session)


@router.get("/{id}/books", response_model=list[BookRead])
def read_books_by_serie(
    id: int,
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(gt=0, le=100)] = 10,
):
    return get_books_by_serie(id, offset, limit, session)
