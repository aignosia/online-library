from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
import numpy as np
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from pwdlib import PasswordHash
from sqlmodel import Session, select

from app.books.models import Book
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


def get_user(username: str, session: Session):
    user = session.get(User, username)
    return user


def authenticate_user(username: str, password: str, session: Session):
    user = get_user(username, session)
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


def get_books_by_user(
    username: str, offset: int | None, limit: int | None, session: Session
):
    books = session.exec(
        select(Book)
        .join(UserBookDownload)
        .join(User)
        .where(User.username == username)
        .offset(offset)
        .limit(limit)
    ).all()
    return books


def update_user_profile(username: str, book_id: int, session: Session):
    user = session.get(User, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    user_books = list(get_books_by_user(username, None, None, session))
    if book in user_books:
        user_books.remove(book)

    if isinstance(user.profile, list):
        user.profile = np.array(user.profile)
    if isinstance(book.embedding, list):
        book.embedding = np.array(book.embedding)

    if user.profile is None:
        user.profile = book.embedding
    else:
        user.profile = (user.profile * len(user_books) + book.embedding) / (
            len(user_books) + 1
        )

    session.add(user)
    session.commit()
    return user


def add_user_download(username: str, book_id: int, session: Session):
    user = session.get(User, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    record_datetime = datetime.now()
    user_download = UserBookDownload(
        username=username, book_id=book_id, dt_record=record_datetime
    )
    response = user_download.model_dump()
    session.add(user_download)
    session.commit()
    session.refresh(user_download)
    return response


def rerank_books(query: list[Book], response: list[Book]):
    reranked_response = response.copy()
    book_languages = [book.language_code for book in query]
    reranked_response.sort(
        key=lambda x: x.language_code in book_languages,
        reverse=True,
    )
    return reranked_response[:10]


def get_user_book_recommmendations(username: str, session: Session):
    user = session.get(User, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    recommendations = session.exec(
        select(Book)
        .order_by(Book.embedding.cosine_distance(user.profile))  # ty:ignore[possibly-missing-attribute]
        .limit(50)
    )
    user_downloads = get_books_by_user(username, None, None, session)
    return rerank_books(user_downloads, list(recommendations))
