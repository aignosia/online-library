from fastapi import APIRouter

from app.config.db import SessionDep
from app.series.models import SerieCreate, SerieRead
from app.series.services import add_serie, get_serie, get_series

router = APIRouter(prefix="/series", tags=["Series"])


@router.post("", response_model=SerieRead)
def create_serie(serie: SerieCreate, session: SessionDep):
    return add_serie(serie, session)


@router.get("", response_model=list[SerieRead])
def read_series(session: SessionDep, offset: int = 0, limit: int = 10):
    return get_series(offset, limit, session)


@router.get("/{id}", response_model=SerieRead)
def read_serie(id: int, session: SessionDep):
    return get_serie(id, session)
