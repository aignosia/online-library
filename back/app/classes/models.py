from typing import TYPE_CHECKING

from sqlmodel import Field, SQLModel
from sqlmodel.main import Relationship

if TYPE_CHECKING:
    from app.subclasses.models import Subclass, SubclassRead


class ClassBase(SQLModel):
    name: str


class Class(ClassBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    subclasses: list["Subclass"] = Relationship(back_populates="_class")


class ClassCreate(ClassBase):
    pass


class ClassRead(ClassBase):
    id: int


class ClassReadWithSubclasses(ClassRead):
    subclasses: list["SubclassRead"] = []
