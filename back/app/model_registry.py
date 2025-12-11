from app.authors.models import AuthorRead, AuthorReadWithBooks
from app.bookclasses.models import (  # noqa: F401
    BookClassRead,
    BookClassReadWithSubclasses,
)
from app.books.models import Book, BookRead, BookReadFull  # noqa: F401
from app.files.models import FileRead, FileReadWithBook
from app.publishers.models import PublisherRead, PublisherReadWithBooks
from app.series.models import SerieRead, SerieReadWithBooks
from app.subclasses.models import (
    SubclassRead,  # noqa: F401
    SubclassReadWithBookClass,
    SubclassReadWithBooks,
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
BookClassReadWithSubclasses.model_rebuild()

PublisherRead.model_rebuild()
SerieRead.model_rebuild()
AuthorRead.model_rebuild()
SubjectRead.model_rebuild()
FileRead.model_rebuild()
SubclassReadWithBookClass.model_rebuild()
BookRead.model_rebuild()
BookReadFull.model_rebuild()
