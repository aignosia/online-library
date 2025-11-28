from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.subjects.models import Subject, SubjectRead


class CategoryBase(SQLModel):
    name: str


class Category(CategoryBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    subjects: list["Subject"] = Relationship(back_populates="category")


class CategoryCreate(CategoryBase):
    pass


class CategoryRead(CategoryBase):
    id: int


class CategoryReadWithSubjects(CategoryRead):
    subjects: list["SubjectRead"] = []
