from fastapi import HTTPException
from sqlmodel import Session, select

from app.categories.models import Category, CategoryCreate


def add_category(category: CategoryCreate, session: Session):
    db_category = Category.model_validate(category)
    session.add(db_category)
    session.commit()
    session.refresh(db_category)
    return db_category


def get_categories(offset: int, limit: int, session: Session):
    categories = session.exec(
        select(Category).offset(offset).limit(limit)
    ).all()
    return categories


def get_category(id: int, session: Session):
    category = session.get(Category, id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
