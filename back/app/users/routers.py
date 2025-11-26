from typing import Annotated

from fastapi import APIRouter, Depends

from app.config.db import SessionDep
from app.users.models import User, UserCreate, UserRead
from app.users.services import add_user, get_current_active_user

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("", response_model=UserRead)
def create_user(user_in: UserCreate, session: SessionDep):
    return add_user(user_in, session)


@router.get("/me", response_model=UserRead)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user


@router.get("/me/items")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return [{"item_id": "Foo", "owner": current_user.username}]
