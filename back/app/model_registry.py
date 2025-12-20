from app.authors.models import AuthorRead
from app.bookclasses.models import (  # noqa: F401
    BookClassRead,
    BookClassReadWithSubclasses,
)
from app.books.models import Book, BookRead, BookReadFull  # noqa: F401
from app.files.models import FileRead, FileReadWithBook
from app.publishers.models import PublisherRead
from app.series.models import SerieRead
from app.subclasses.models import (
    SubclassRead,  # noqa: F401
    SubclassReadWithBookClass,
)
from app.subjects.models import SubjectRead

FileReadWithBook.model_rebuild()
BookClassReadWithSubclasses.model_rebuild()

PublisherRead.model_rebuild()
SerieRead.model_rebuild()
AuthorRead.model_rebuild()
SubjectRead.model_rebuild()
FileRead.model_rebuild()
SubclassReadWithBookClass.model_rebuild()
BookRead.model_rebuild()
BookReadFull.model_rebuild()
