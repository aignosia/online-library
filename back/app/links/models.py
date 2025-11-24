from sqlmodel import Field, SQLModel


class BookAuthorLink(SQLModel, table=True):
    book_id: int = Field(default=None, primary_key=True, foreign_key="book.id")
    author_id: int = Field(
        default=None, primary_key=True, foreign_key="author.id"
    )
