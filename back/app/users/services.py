import math
from datetime import datetime, timedelta, timezone
from typing import Annotated
from uuid import UUID

import jwt
import numpy as np
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from pwdlib import PasswordHash
from sqlmodel import Session, func, select

from app.books.models import Book, BookRead
from app.config.config import settings
from app.config.db import SessionDep
from app.links.models import UserBookDownload
from app.users.models import TokenData, User, UserCreate

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

password_hash = PasswordHash.recommended()


def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password):
    return password_hash.hash(password)


def add_user(user_in: UserCreate, session: Session):
    db_user = User.model_validate(
        user_in, update={"hashed_password": get_password_hash(user_in.password)}
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def get_user(email: str, session: Session):
    user = session.exec(select(User).where(User.email == email)).one_or_none()
    return user


def authenticate_user(email: str, password: str, session: Session):
    user = get_user(email, session)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm=settings.PASSWORD_HASH_ALGORITHM,
    )
    return encoded_jwt


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], session: SessionDep
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.PASSWORD_HASH_ALGORITHM],
        )
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception

    user = get_user(token_data.username, session)
    if user is None:
        raise credentials_exception

    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_books_by_user(id: UUID, offset: int, limit: int, session: Session):
    books = session.exec(
        select(Book)
        .join(UserBookDownload)
        .join(User)
        .where(User.id == id)
        .group_by(UserBookDownload.dt_record, Book.id)  # ty:ignore[invalid-argument-type]
        .order_by(UserBookDownload.dt_record)  # ty:ignore[invalid-argument-type]
        .offset(offset)
        .limit(limit)
    ).all()
    books = [BookRead.model_validate(book) for book in books]
    book_count = session.exec(
        select(func.count())
        .select_from(Book)
        .join(UserBookDownload)
        .join(User)
        .where(User.id == id)
        .group_by(UserBookDownload.dt_record, Book.id)
    ).one_or_none()
    if book_count is None:
        book_count = 0
    print(limit)
    max_offset = max(math.ceil(float(book_count / limit)) - 1, 0)
    return {"total_books": book_count, "max_offset": max_offset, "books": books}


def get_user_download_count(id: UUID, session: Session):
    count = session.exec(
        select(func.count())
        .select_from(Book)
        .join(UserBookDownload)
        .join(User)
        .where(User.id == id)
        .group_by(UserBookDownload.dt_record, Book.id)
    ).one_or_none()
    if count is None:
        count = 0
    return count


def update_user_profile(
    profile: np.ndarray | None, embedding: np.ndarray, download_num: int
):
    if profile is None:
        new_profile = embedding
    else:
        new_profile = (profile * download_num + embedding) / (download_num + 1)

    return new_profile


def add_user_download(id: UUID, book_id: int, session: Session):
    user = session.get(User, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    record_datetime = datetime.now()
    user_download = UserBookDownload(
        user_id=id, book_id=book_id, dt_record=record_datetime
    )
    response = user_download.model_dump()
    session.add(user_download)
    profile = (
        np.array(user.profile)
        if isinstance(user.profile, list)
        else user.profile
    )
    embedding = (
        np.array(book.embedding)
        if isinstance(book.embedding, list)
        else book.embedding or np.ndarray([])
    )
    download_num = get_user_download_count(user.id, session) - 1
    new_profile = update_user_profile(profile, embedding, download_num)
    user.profile = new_profile
    session.add(user)
    session.commit()
    session.refresh(user_download)
    return response


def rerank_books(query: list[Book], response: list[Book], limit: int):
    reranked_response = response.copy()
    book_languages = [book.language_code for book in query]
    reranked_response.sort(
        key=lambda x: x.language_code in book_languages,
        reverse=True,
    )
    reranked_response = list(
        filter(lambda x: x not in query, reranked_response)
    )
    return reranked_response[:limit]


def get_user_book_recommmendations(id: UUID, limit: int, session: Session):
    user = session.get(User, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    recommendations = session.exec(
        select(Book)
        .order_by(Book.embedding.cosine_distance(user.profile))  # ty:ignore[possibly-missing-attribute]
        .limit(limit + 50)
    ).all()
    user_downloads = get_books_by_user(
        id, 0, max(get_user_download_count(id, session), 1), session
    ).get("books")
    recommendations = [
        BookRead.model_validate(book)
        for book in rerank_books(user_downloads, list(recommendations), limit)
    ]
    return recommendations
