from fastapi import APIRouter

from app.books.models import BookCreate, BookRead
from app.books.services import add_book, get_book, get_books
from app.config.db import SessionDep

router = APIRouter(prefix="/books", tags=["Books"])


@router.post("", response_model=BookRead)
def create_book(book: BookCreate, session: SessionDep):
    return add_book(book, session)


@router.get("", response_model=list[BookRead])
def read_books(session: SessionDep, offset: int = 0, limit: int = 10):
    return get_books(offset, limit, session)


@router.get("/{id}", response_model=BookRead)
def read_book(id: int, session: SessionDep):
    return get_book(id, session)
