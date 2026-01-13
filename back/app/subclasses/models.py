from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from app.links.models import BookSubclassLink

if TYPE_CHECKING:
    from app.bookclasses.models import BookClass, BookClassRead
    from app.books.models import Book


class SubclassBase(SQLModel):
    name: str

    bookclass_id: int | None = Field(default=None, foreign_key="bookclass.id")


class Subclass(SubclassBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    books: list["Book"] = Relationship(
        back_populates="subclasses", link_model=BookSubclassLink
    )
    bookclass: "BookClass" = Relationship(back_populates="subclasses")


class SubclassCreate(SubclassBase):
    pass


class SubclassRead(SubclassBase):
    id: int


class SubclassReadWithBookClass(SubclassRead):
    bookclass: Optional["BookClassRead"] = None
