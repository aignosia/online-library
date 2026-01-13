from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.books.models import Book


class FileBase(SQLModel):
    type: str
    label: str
    location: str

    book_id: int | None = Field(default=None, foreign_key="book.id")


class File(FileBase, table=True):
    id: int = Field(default=None, primary_key=True)

    book: "Book" = Relationship(back_populates="files")


class FileCreate(FileBase):
    pass


class FileRead(FileBase):
    id: int


class FileReadWithBook(FileBase):
    book: Optional["Book"] = None
