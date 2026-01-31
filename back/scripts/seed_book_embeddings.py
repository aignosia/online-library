import joblib
import typer
from sqlmodel import Session, select

from app.books.models import Book
from app.books.services import get_book_tfidf_text
from app.config.config import settings
from app.config.db import engine


def seed_book_embeddings():
    with Session(engine) as session:
        tfidf = joblib.load(settings.RECOMMENDATION_MODEL_FILE)
        batch_size = 10000
        statement = select(Book).execution_options(yield_per=batch_size)
        treated_books = 0
        for book in session.exec(statement):
            book_text = get_book_tfidf_text(book)
            book.embedding = tfidf.transform([book_text]).toarray()[0]
            session.add(book)
            treated_books += 1
            print("Treated books", treated_books, flush=True)
            print("\033[F\033[K", end="")

        print("Commiting books...")
        session.commit()
        typer.echo(f"Treated books: {treated_books}")
