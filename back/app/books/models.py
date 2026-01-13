from typing import TYPE_CHECKING, Optional

from sqlmodel import JSON, Column, Field, Relationship, SQLModel

from app.links.models import (
    BookAuthorLink,
    BookSubclassLink,
    BookSubjectLink,
    UserBookDownload,
)
from app.subclasses.models import SubclassReadWithBookClass

if TYPE_CHECKING:
    from app.authors.models import Author, AuthorRead
    from app.files.models import File, FileRead
    from app.publishers.models import Publisher, PublisherRead
    from app.series.models import Serie, SerieRead
    from app.subclasses.models import Subclass
    from app.subjects.models import Subject, SubjectRead
    from app.users.models import User


class BookBase(SQLModel):
    title: str
    pub_year: int
    summary: str
    isbn: str | None = None
    notes: list[str] = Field(default=[], sa_column=Column(JSON))
    language_code: str | None = None
    cover: str | None = None

    publisher_id: int | None = Field(default=None, foreign_key="publisher.id")
    serie_id: int | None = Field(default=None, foreign_key="serie.id")


class Book(BookBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    publisher: Optional["Publisher"] = Relationship(back_populates="books")
    serie: Optional["Serie"] = Relationship(back_populates="books")
    authors: list["Author"] = Relationship(
        back_populates="books", link_model=BookAuthorLink
    )
    subjects: list["Subject"] = Relationship(
        back_populates="books", link_model=BookSubjectLink
    )
    files: list["File"] = Relationship(back_populates="book")
    users: list["User"] = Relationship(
        back_populates="books", link_model=UserBookDownload
    )
    subclasses: list["Subclass"] = Relationship(
        back_populates="books", link_model=BookSubclassLink
    )


class BookCreate(BookBase):
    id: int | None


class BookRead(SQLModel):
    id: int
    title: str
    pub_year: int
    authors: list["AuthorRead"] = []
    cover: str | None


class BookReadFromAuthor(SQLModel):
    id: int
    title: str
    pub_year: int


class BookReadFull(BookBase):
    publisher: Optional["PublisherRead"] = None
    serie: Optional["SerieRead"] = None
    authors: list["AuthorRead"] = []
    subjects: list["SubjectRead"] = []
    files: list["FileRead"] = []
    subclasses: list["SubclassReadWithBookClass"] = []
