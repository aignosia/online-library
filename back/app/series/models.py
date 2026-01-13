from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.books.models import Book


class SerieBase(SQLModel):
    name: str


class Serie(SerieBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    books: list["Book"] = Relationship(back_populates="serie")


class SerieCreate(SerieBase):
    pass


class SerieRead(SerieBase):
    id: int
