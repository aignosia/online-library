from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from app.links.models import BookSubclassLink

if TYPE_CHECKING:
    from app.books.models import Book, BookRead
    from app.classes.models import Class, ClassRead


class SubclassBase(SQLModel):
    name: str

    class_id: int | None = Field(default=None, foreign_key="class.id")


class Subclass(SubclassBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    books: list["Book"] = Relationship(
        back_populates="subclasses", link_model=BookSubclassLink
    )
    _class: "Class" = Relationship(back_populates="subclasses")


class SubclassCreate(SubclassBase):
    pass


class SubclassRead(SubclassBase):
    id: int


class SubclassReadWithBooks(SubclassRead):
    books: list["BookRead"] = []


class SubclassReadWithClass(SubclassRead):
    _class: Optional["ClassRead"] = None
