from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.authors.models import Author
    from app.publishers.models import Publisher, PublisherRead
    from app.series.models import Serie, SerieRead

from app.links.models import BookAuthorLink
from app.publishers.models import PublisherReadWithBooks


class BookBase(SQLModel):
    title: str
    pub_year: int
    summary: str
    isbn: str
    uniform_title: str | None = None
    general_note: str | None = None
    fc_note: str | None = None
    credits_note: str | None = None
    ov_note: str | None = None
    language_note: str | None = None

    publisher_id: int | None = Field(default=None, foreign_key="publisher.id")
    serie_id: int | None = Field(default=None, foreign_key="serie.id")


class Book(BookBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    publisher: Optional["Publisher"] = Relationship(back_populates="books")
    serie: Optional["Serie"] = Relationship(back_populates="books")
    authors: list["Author"] = Relationship(
        back_populates="books", link_model=BookAuthorLink
    )


class BookCreate(BookBase):
    id: int | None


class BookRead(SQLModel):
    id: int
    title: str
    pub_year: int
    author: str | None = None


class BookReadFromAuthor(SQLModel):
    id: int
    title: str
    pub_year: int


class BookReadFull(BookBase):
    publisher: Optional["PublisherRead"] = None
    serie: Optional["SerieRead"] = None


PublisherReadWithBooks.model_rebuild()
