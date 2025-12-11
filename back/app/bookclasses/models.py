from typing import TYPE_CHECKING

from sqlmodel import Field, SQLModel
from sqlmodel.main import Relationship

if TYPE_CHECKING:
    from app.subclasses.models import Subclass, SubclassRead


class BookClassBase(SQLModel):
    name: str


class BookClass(BookClassBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    subclasses: list["Subclass"] = Relationship(back_populates="bookclass")


class BookClassCreate(BookClassBase):
    pass


class BookClassRead(BookClassBase):
    id: int


class BookClassReadWithSubclasses(BookClassRead):
    subclasses: list["SubclassRead"] = []
