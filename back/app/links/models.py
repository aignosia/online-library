from datetime import datetime

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
    username: str = Field(
        default=None, primary_key=True, foreign_key="user.username"
    )
    book_id: int = Field(default=None, primary_key=True, foreign_key="book.id")
    dt_record: datetime
