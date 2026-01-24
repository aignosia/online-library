import spacy
from fastapi import HTTPException
from sqlmodel import Session, func, or_, select

from app.authors.models import Author
from app.books.models import Book, BookCreate
from app.links.models import BookAuthorLink, UserBookDownload
from app.recmodel.services import compute_embedding


def merge_names(text: str) -> str:
    spacy_model = "xx_ent_wiki_sm"
    nlp = spacy.load(spacy_model)
    doc = nlp(text)
    with doc.retokenize() as retokenizer:
        for ent in doc.ents:
            new_text = ent.text.replace(" ", "_")
            retokenizer.merge(ent, attrs={"LEMMA": new_text})

    return " ".join([t.lemma_ if t.lemma_ != t.text else t.text for t in doc])


def get_book_tfidf_text(book: Book) -> str:
    authors_str = " | ".join(
        f"{a.firstname + ' ' if a.firstname else ''}{a.lastname}"
        for a in book.authors
    )
    subjects_str = " | ".join(s.name for s in book.subjects)
    bookclasses_str = " | ".join(s.bookclass.name for s in book.subclasses)
    subclasses_str = " | ".join(s.name for s in book.subclasses)
    text = " | ".join(
        [
            authors_str,
            book.title,
            book.summary,
            subjects_str,
            bookclasses_str,
            subclasses_str,
        ]
    )
    return text


def add_book(book: BookCreate, session: Session):
    db_book = Book.model_validate(book)
    book_tfidf_text = get_book_tfidf_text(db_book)
    book_tfidf_text = merge_names(book_tfidf_text)
    book.embedding = compute_embedding(book_tfidf_text)
    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return db_book


def get_books(offset: int, limit: int, session: Session):
    books = session.exec(select(Book).offset(offset).limit(limit)).all()
    return books


def get_book(id: int, session: Session):
    book = session.get(Book, id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    return book


def get_books_search(q: str, session: Session):
    query_term = " & ".join(f"{word}" for word in q.split())
    ts_query = func.to_tsquery("simple", query_term)

    book_vector = func.to_tsvector("simple", func.coalesce(Book.title, ""))
    author_vector = func.to_tsvector(
        "simple",
        func.coalesce(Author.firstname, "")
        + " "
        + func.coalesce(Author.lastname),
    )

    results = session.exec(
        select(Book)
        .outerjoin(BookAuthorLink)
        .outerjoin(Author)
        .where(
            or_(
                book_vector.op("@@")(ts_query),
                author_vector.op("@@")(ts_query),
            )
        )
        .group_by(Book.id)  # ty:ignore[invalid-argument-type]
    ).all()

    return results


def get_search_autocomplete(q: str, session: Session):
    query_term = " & ".join(f"{word}:*" for word in q.split())
    ts_query = func.to_tsquery("simple", query_term)

    book_tsvector = func.to_tsvector("simple", func.coalesce(Book.title, ""))
    author_tsvector = func.to_tsvector(
        "simple",
        func.coalesce(Author.firstname, "")
        + " "
        + func.coalesce(Author.lastname, ""),
    )

    results = list(
        session.exec(
            select(Book.title).where(book_tsvector.op("@@")(ts_query))
        ).all()
    ) + list(
        " ".join(e for e in it if e is not None)
        for it in session.exec(
            select(Author.firstname, Author.lastname).where(
                author_tsvector.op("@@")(ts_query)
            )
        ).all()
    )

    return list(dict.fromkeys(results[:10]))


def get_book_count(session: Session):
    count = session.exec(select(func.count()).select_from(Book)).one()
    return count


def get_popular_books(offset: int, limit: int, session: Session):
    subquery = (
        select(
            UserBookDownload.book_id,
            func.count(UserBookDownload.book_id).label("download"),
        )
        .group_by(UserBookDownload.book_id)
        .offset(offset)
        .limit(limit)
        .subquery()
    )
    books = session.exec(
        select(Book)
        .outerjoin(subquery)
        .order_by(
            func.coalesce(subquery.c.download, 0).label("download").desc()
        )
        .offset(offset)
        .limit(limit)
    ).all()
    return books


def rerank_books(query: Book, response: list[Book], limit: int):
    reranked_response = response.copy()
    reranked_response.sort(
        key=lambda x: x.language_code == query.language_code, reverse=True
    )
    if query in response:
        reranked_response.remove(query)
    return reranked_response[:limit]


def get_similar_books(id: int, limit: int, session: Session):
    book = session.get(Book, id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    similar_books = session.exec(
        select(Book)
        .where(Book.id != book.id)
        .order_by(Book.embedding.cosine_distance(book.embedding))  # ty:ignore[possibly-missing-attribute]
        .limit(limit + 50)
    ).all()
    return rerank_books(book, list(similar_books), limit)
