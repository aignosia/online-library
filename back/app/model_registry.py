from app.authors.models import AuthorRead, AuthorReadWithBooks
from app.books.models import Book, BookRead, BookReadFull  # noqa: F401
from app.classes.models import ClassReadWithSubclasses
from app.files.models import FileRead, FileReadWithBook
from app.publishers.models import PublisherRead, PublisherReadWithBooks
from app.series.models import SerieRead, SerieReadWithBooks
from app.subclasses.models import (
    SubclassRead,  # noqa: F401
    SubclassReadWithBooks,
    SubclassReadWithClass,
)
from app.subjects.models import SubjectRead, SubjectReadWithBooks
from app.users.models import UserReadWithBooks

PublisherReadWithBooks.model_rebuild()
AuthorReadWithBooks.model_rebuild()
FileReadWithBook.model_rebuild()
SerieReadWithBooks.model_rebuild()
SubjectReadWithBooks.model_rebuild()
UserReadWithBooks.model_rebuild()
SubclassReadWithBooks.model_rebuild()
ClassReadWithSubclasses.model_rebuild()

PublisherRead.model_rebuild()
SerieRead.model_rebuild()
AuthorRead.model_rebuild()
SubjectRead.model_rebuild()
FileRead.model_rebuild()
SubclassReadWithClass.model_rebuild()
BookRead.model_rebuild()
BookReadFull.model_rebuild()
