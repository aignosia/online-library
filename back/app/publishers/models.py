from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.books.models import Book, BookRead


class PublisherBase(SQLModel):
    name: str


class Publisher(PublisherBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    books: list["Book"] = Relationship(back_populates="publisher")  # noqa: F821


class PublisherCreate(PublisherBase):
    pass


class PublisherRead(PublisherBase):
    id: int


class PublisherReadWithBooks(PublisherBase):
    id: int
    books: list["BookRead"] = []  # noqa: F821
