from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session
from starlette.requests import Request

from app.config.config import default


class Base(DeclarativeBase): ...


engine = create_engine(default.db_url, pool_size=5, max_overflow=5)


def get_db(request: Request):
    return request.state.db


DbSession = Annotated[Session, Depends(get_db)]
