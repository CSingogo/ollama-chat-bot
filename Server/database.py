from typing import Annotated, Generator
from sqlmodel import  (
    create_engine, 
    Session,
    SQLModel
)
from fastapi import Depends
from sqlalchemy.orm import sessionmaker
from models.user_model import User

DATABASE_URL = "sqlite:///database.db"

# engine = create_engine(DATABASE_URL, echo=True)

# def create_db_and_tables():  
#     SQLModel.metadata.create_all(engine)

# def get_session():
#     with Session(engine) as session:
#         yield session

# SessionDep = Annotated[Session, Depends(get_session)]

engine = create_engine(
    DATABASE_URL, 
    echo=True, 
    connect_args={"check_same_thread": False} # Required for SQLite + FastAPI
)

SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine, 
    class_=Session  # This tells it to use SQLModel's Session wrapper
)

def get_session() -> Generator[Session, None, None]:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
SessionDep = Annotated[Session, Depends(get_session)]


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
