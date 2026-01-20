from contextlib import contextmanager
from typing import Annotated
from fastapi import Depends
from sqlmodel import Session
from config.database import SessionLocal


@contextmanager
def get_session() -> Session: # type: ignore
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

SessionDep = Annotated[Session, Depends[get_session]]