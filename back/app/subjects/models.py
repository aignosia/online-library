from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from app.categories.models import CategoryReadWithSubjects
from app.links.models import BookSubjectLink

if TYPE_CHECKING:
    from app.books.models import Book, BookRead
    from app.categories.models import Category


class SubjectBase(SQLModel):
    name: str

    category_id: int | None = Field(default=None, foreign_key="category.id")


class Subject(SubjectBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    books: list["Book"] = Relationship(
        back_populates="subjects", link_model=BookSubjectLink
    )
    category: Optional["Category"] = Relationship(back_populates="subjects")


class SubjectCreate(SubjectBase):
    pass


class SubjectRead(SubjectBase):
    id: int


class SubjectReadWithBooks(SubjectRead):
    books: list["BookRead"] = []


CategoryReadWithSubjects.model_rebuild()
