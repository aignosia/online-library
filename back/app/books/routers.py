from typing import Annotated

from fastapi import APIRouter, Query

from app.books.models import BookCreate, BookRead, BookReadFull
from app.books.services import (
    add_book,
    get_book,
    get_book_count,
    get_books,
    get_books_search,
    get_popular_books,
    get_search_autocomplete,
    get_similar_books,
)
from app.config.db import SessionDep

router = APIRouter(prefix="/books", tags=["Books"])


@router.post("", response_model=BookRead)
def create_book(book: BookCreate, session: SessionDep):
    return add_book(book, session)


@router.get("", response_model=list[BookRead])
def read_books(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 10,
):
    return get_books(offset, limit, session)


@router.get("/search", response_model=list[BookRead])
def search_books(
    session: SessionDep,
    q: Annotated[str, Query(min_length=2)],
):
    return get_books_search(q, session)


@router.get("/autocomplete")
def autocomplete_search(
    session: SessionDep,
    q: Annotated[str, Query(min_length=2)],
):
    return get_search_autocomplete(q, session)


@router.get("/count")
def read_book_count(session: SessionDep):
    count = get_book_count(session)
    return {"resource": "book", "count": count}


@router.get("/popular", response_model=list[BookRead])
def read_popular_book(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(lt=100)] = 10,
):
    return get_popular_books(offset, limit, session)


@router.get("/{id}", response_model=BookReadFull)
def read_book(id: int, session: SessionDep):
    return get_book(id, session)


@router.get("/{id}/recommendations", response_model=list[BookRead])
def read_similar_book_recommendations(
    id: int,
    session: SessionDep,
    limit: Annotated[int, Query(le=100)] = 10,
):
    return get_similar_books(id, limit, session)
