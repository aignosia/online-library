from fastapi import APIRouter

from app.authors.models import AuthorCreate, AuthorRead
from app.authors.services import add_author, get_author, get_authors
from app.config.db import SessionDep

router = APIRouter(prefix="/authors", tags=["Authors"])


@router.post("", response_model=AuthorRead)
def create_author(author: AuthorCreate, session: SessionDep):
    return add_author(author, session)


@router.get("", response_model=list[AuthorRead])
def read_authors(session: SessionDep, offset: int = 0, limit: int = 10):
    return get_authors(offset, limit, session)


@router.get("/{id}", response_model=AuthorRead)
def read_author(id: int, session: SessionDep):
    return get_author(id, session)
