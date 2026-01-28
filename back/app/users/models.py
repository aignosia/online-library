from typing import TYPE_CHECKING, Any
from uuid import UUID, uuid4

from pgvector.sqlalchemy import Vector
from pydantic import BaseModel, EmailStr
from sqlmodel import Field, SQLModel
from sqlmodel.main import Relationship

from app.links.models import UserBookDownload

if TYPE_CHECKING:
    from app.books.models import Book


class UserBase(SQLModel):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: EmailStr = Field(unique=True, max_length=255)
    full_name: str | None = Field(default=None, max_length=255)
    is_active: bool | None = True


class User(UserBase, table=True):
    hashed_password: str
    profile: Any | None = Field(default=None, sa_type=Vector(10000))

    books: list["Book"] = Relationship(
        back_populates="users", link_model=UserBookDownload
    )


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=128)


class UserRead(UserBase):
    pass


class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserRead


class TokenData(BaseModel):
    username: str
