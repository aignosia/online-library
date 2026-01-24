from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.books.models import BookRead
from app.config.db import SessionDep
from app.users.models import User, UserCreate, UserRead
from app.users.services import (
    add_user,
    add_user_download,
    get_books_by_user,
    get_current_active_user,
    get_user_book_recommmendations,
    update_user_profile,
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
    limit: Annotated[int | None, Query(le=100)] = None,
):
    return get_books_by_user(current_user.username, offset, limit, session)


@router.get("/me/books/recommendations", response_model=list[BookRead])
async def read_own_book_recommendations(
    current_user: Annotated[User, Depends(get_current_active_user)],
    session: SessionDep,
    limit: Annotated[int, Query(le=100)] = 10,
):
    return get_user_book_recommmendations(current_user.username, limit, session)


@router.post("/me/books/{id}")
async def add_own_book_download(
    id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    session: SessionDep,
):
    user_download = add_user_download(current_user.username, id, session)
    update_user_profile(current_user.username, id, session)
    return user_download
