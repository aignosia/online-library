from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.config import config
from app.config.db import SessionDep
from app.users.models import Token, UserRead
from app.users.services import authenticate_user, create_access_token

router = APIRouter(tags=["Users"])


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: SessionDep,
) -> Token:
    user = authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(
        days=config.settings.ACCESS_TOKEN_EXPIRE_DAYS
    )
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    user_read = UserRead.model_validate(user)
    return Token(access_token=access_token, token_type="bearer", user=user_read)
