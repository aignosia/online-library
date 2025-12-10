from fastapi import APIRouter

from app.config.db import SessionDep
from app.subclasses.models import (
    SubclassCreate,
    SubclassRead,
    SubclassReadWithBooks,
)
from app.subclasses.services import add_subclass, get_subclass, get_subclasses

router = APIRouter(prefix="/subclasses", tags=["Subclasses"])


@router.post("", response_model=SubclassRead)
def create_subclass(subclass: SubclassCreate, session: SessionDep):
    return add_subclass(subclass, session)


@router.get("", response_model=list[SubclassRead])
def read_subclasses(session: SessionDep, offset: int = 0, limit: int = 10):
    return get_subclasses(offset, limit, session)


@router.get("/{id}", response_model=SubclassReadWithBooks)
def read_subclass(id: int, session: SessionDep):
    return get_subclass(id, session)
