from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from app.links.models import BookSubclassLink

if TYPE_CHECKING:
    from app.books.models import Book, BookRead


class SubclassBase(SQLModel):
    name: str


class Subclass(SubclassBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    books: list["Book"] = Relationship(
        back_populates="subclasses", link_model=BookSubclassLink
    )


class SubclassCreate(SubclassBase):
    pass


class SubclassRead(SubclassBase):
    id: int


class SubclassReadWithBooks(SubclassRead):
    books: list["BookRead"]
