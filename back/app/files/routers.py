from fastapi import APIRouter

from app.config.db import SessionDep
from app.files.models import FileCreate, FileRead, FileReadWithBook
from app.files.services import add_file, get_file, get_files

router = APIRouter(prefix="/files", tags=["Files"])


@router.post("", response_model=FileRead)
def create_file(file: FileCreate, session: SessionDep):
    return add_file(file, session)


@router.get("", response_model=list[FileRead])
def read_files(session: SessionDep, offset: int, limit: int):
    return get_files(offset, limit, session)


@router.get("/{id}", response_model=FileReadWithBook)
def read_file(id: int, session: SessionDep):
    return get_file(id, session)
