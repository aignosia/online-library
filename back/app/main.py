from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import model_registry  # noqa: F401
from app.authors.routers import router as authors_router
from app.bookclasses.routers import router as classes_router
from app.books.routers import router as books_router
from app.config.config import settings
from app.config.db import init_db
from app.files.routers import router as files_router
from app.publishers.routers import router as publisher_router
from app.series.routers import router as series_router
from app.subclasses.routers import router as subclasses_router
from app.subjects.routers import router as subjects_router
from app.users.auth import router as auth_router
from app.users.routers import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,  # ty:ignore[invalid-argument-type]
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router)
app.include_router(auth_router)
app.include_router(books_router)
app.include_router(publisher_router)
app.include_router(series_router)
app.include_router(authors_router)
app.include_router(subjects_router)
app.include_router(files_router)
app.include_router(subclasses_router)
app.include_router(classes_router)
