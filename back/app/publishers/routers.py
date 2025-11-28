from fastapi import APIRouter

from app.config.db import SessionDep
from app.publishers.models import (
    PublisherCreate,
    PublisherRead,
    PublisherReadWithBooks,
)
from app.publishers.services import add_publisher, get_publisher, get_publishers

router = APIRouter(prefix="/publishers", tags=["Publishers"])


@router.post("", response_model=PublisherRead)
def create_publisher(publisher: PublisherCreate, session: SessionDep):
    return add_publisher(publisher, session)


@router.get("", response_model=list[PublisherRead])
def read_publishers(session: SessionDep, offset: int = 0, limit: int = 10):
    return get_publishers(offset, limit, session)


@router.get("/{id}")
def read_publisher(id: int, session: SessionDep):
    publisher = PublisherReadWithBooks.model_validate(
        get_publisher(id, session)
    )
    return publisher
