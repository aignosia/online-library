from app.authors.models import Author, AuthorRead
from app.bookclasses.models import (  # noqa: F401
    BookClassRead,
    BookClassReadWithSubclasses,
)
from app.books.models import (  # noqa: F401
    Book,
    BookCreate,
    BookRead,
    BookReadFull,
)
from app.files.models import File, FileRead, FileReadWithBook  # noqa: F401
from app.publishers.models import Publisher, PublisherRead  # noqa: F401
from app.series.models import Serie, SerieRead  # noqa: F401
from app.subclasses.models import (
    Subclass,  # noqa: F401
    SubclassRead,  # noqa: F401
    SubclassReadWithBookClass,
)
from app.subjects.models import Subject, SubjectRead  # noqa: F401
from app.users.models import User  # noqa: F401

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
BookCreate.model_rebuild()
