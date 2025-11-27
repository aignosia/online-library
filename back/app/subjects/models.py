from typing import TYPE_CHECKING

from sqlmodel import SQLModel
from sqlmodel.main import Field, Relationship

from app.links.models import BookSubjectLink

if TYPE_CHECKING:
    from app.books.models import Book, BookRead


class SubjectBase(SQLModel):
    name: str


class Subject(SubjectBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    books: list["Book"] = Relationship(
        back_populates="subjects", link_model=BookSubjectLink
    )


class SubjectCreate(SubjectBase):
    pass


class SubjectRead(SubjectBase):
    id: int


class SubjectReadWithBooks(SubjectRead):
    books: list["BookRead"] = []
