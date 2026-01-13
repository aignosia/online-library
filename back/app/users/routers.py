from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.books.models import BookRead
from app.config.db import SessionDep
from app.users.models import User, UserCreate, UserRead
from app.users.services import (
    add_user,
    get_books_by_user,
    get_current_active_user,
)

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("", response_model=UserRead)
def create_user(user: UserCreate, session: SessionDep):
    return add_user(user, session)


@router.get("/me", response_model=UserRead)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user


@router.get("/me/books", response_model=list[BookRead])
async def read_own_book_downloads(
    current_user: Annotated[User, Depends(get_current_active_user)],
    session: SessionDep,
    offset: int | None = None,
    limit: Annotated[int | None, Query(le=100)] = 10,
):
    return get_books_by_user(current_user.username, offset, limit, session)
