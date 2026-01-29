from datetime import datetime
from uuid import UUID

from sqlmodel import Field, SQLModel


class BookAuthorLink(SQLModel, table=True):
    book_id: int = Field(default=None, primary_key=True, foreign_key="book.id")
    author_id: int = Field(
        default=None, primary_key=True, foreign_key="author.id"
    )


class BookSubjectLink(SQLModel, table=True):
    book_id: int = Field(default=None, primary_key=True, foreign_key="book.id")
    subject_id: int = Field(
        default=None, primary_key=True, foreign_key="subject.id"
    )


class UserBookDownload(SQLModel, table=True):
    user_id: UUID = Field(default=None, primary_key=True, foreign_key="user.id")
    book_id: int = Field(default=None, primary_key=True, foreign_key="book.id")
    dt_record: datetime = Field(default=None, primary_key=True)


class BookSubclassLink(SQLModel, table=True):
    book_id: int = Field(default=None, primary_key=True, foreign_key="book.id")
    subclass_id: int = Field(
        default=None, primary_key=True, foreign_key="subclass.id"
    )
