from fastapi import APIRouter

from app.categories.models import (
    CategoryCreate,
    CategoryRead,
    CategoryReadWithSubjects,
)
from app.categories.services import add_category, get_categories, get_category
from app.config.db import SessionDep

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.post("", response_model=CategoryRead)
def create_category(category: CategoryCreate, session: SessionDep):
    return add_category(category, session)


@router.get("", response_model=list[CategoryRead])
def read_categories(session: SessionDep, offset: int = 0, limit: int = 10):
    return get_categories(offset, limit, session)


@router.get("/{id}", response_model=CategoryReadWithSubjects)
def read_category(id: int, session: SessionDep):
    return get_category(id, session)
