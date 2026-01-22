import joblib
import spacy
import typer
from sklearn.feature_extraction.text import TfidfVectorizer
from spacy.language import Language
from spacy.tokens import Doc
from sqlmodel import Session, select
from tqdm import tqdm

from app.books.models import Book
from app.books.services import get_book_tfidf_text
from app.config.db import engine


def merge_entity(doc: Doc) -> str:
    with doc.retokenize() as retokenizer:
        for ent in doc.ents:
            new_text = ent.text.replace(" ", "_")
            retokenizer.merge(ent, attrs={"LEMMA": new_text})

    return " ".join([t.lemma_ if t.lemma_ != t.text else t.text for t in doc])


def compute_books_embeddings(
    books: list[Book], nlp: Language, model: TfidfVectorizer
) -> list[list[float]]:
    texts = [
        get_book_tfidf_text(v)
        for v in tqdm(books, total=len(books), desc="Text")
    ]
    print("\033[F\033[K", end="", flush=True)
    docs = nlp.pipe(texts, n_process=-1, batch_size=50)
    docs_ner = [
        merge_entity(doc) for doc in tqdm(docs, total=len(texts), desc="NER")
    ]
    embeddings = []
    print("\033[F\033[K", end="", flush=True)
    for i in tqdm(range(0, len(docs_ner), 50), desc="Embeddings"):
        embeddings += model.transform(docs_ner[i : i + 50]).toarray().tolist()
    return embeddings


def seed_book_embeddings(model: str):
    typer.echo("Updating book embeddings")
    with Session(engine) as session:
        books = []
        n_treated = 0
        nlp = spacy.load("xx_ent_wiki_sm")
        tfidf = joblib.load(model)
        batch_size = 1000
        statement = select(Book).execution_options(yield_per=batch_size)
        books = []
        for book in session.exec(statement):
            books.append(book)
            if len(books) == batch_size:
                typer.echo(f"Treated books: {n_treated}")
                embeddings = compute_books_embeddings(books, nlp, tfidf)
                for b, embedding in zip(books, embeddings):
                    b.embedding = embedding
                session.add_all(books)
                n_treated += len(books)
                books = []
                for i in range(2):
                    print("\033[F\033[K", end="", flush=True)

        typer.echo(f"Treated books: {n_treated}")
