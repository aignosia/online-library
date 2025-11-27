from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from app.links.models import BookAuthorLink

if TYPE_CHECKING:
    from app.books.models import Book, BookRead


class AuthorBase(SQLModel):
    firstname: str
    lastname: str
    birth_year: int | None = Field(default=None)
    death_year: int | None = Field(default=None)
    fuller_name: str | None = Field(default=None)


class Author(AuthorBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    books: list["Book"] = Relationship(
        back_populates="authors", link_model=BookAuthorLink
    )


class AuthorCreate(AuthorBase):
    pass


class AuthorRead(AuthorBase):
    id: int


class AuthorReadWithBooks(AuthorBase):
    id: int
    books: list["BookRead"] = []
