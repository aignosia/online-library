from fastapi import APIRouter

from app.classes.models import ClassCreate, ClassRead, ClassReadWithSubclasses
from app.classes.services import add_class, get_class, get_classes
from app.config.db import SessionDep

router = APIRouter(prefix="/classes", tags=["Classes"])


@router.post("", response_model=ClassRead)
def create_class(_class: ClassCreate, session: SessionDep):
    return add_class(_class, session)


@router.get("", response_model=list[ClassRead])
def read_classes(session: SessionDep, offset: int = 0, limit: int = 10):
    return get_classes(offset, limit, session)


@router.get("/{id}", response_model=ClassReadWithSubclasses)
def read_class(id: int, session: SessionDep):
    return get_class(id, session)
