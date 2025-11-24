from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.books.models import Book, BookRead


class SerieBase(SQLModel):
    name: str


class Serie(SerieBase):
    id: int | None = Field(default=None, primary_key=True)

    books: list["Book"] = Relationship(back_populates="serie")


class SerieCreate(SerieBase):
    pass


class SerieRead(SerieBase):
    id: int


class SerieReadWithBooks(SerieBase):
    id: int
    books: list["BookRead"] = []
