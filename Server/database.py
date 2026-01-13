from typing import Annotated
from sqlmodel import  create_engine, Session, SQLModel
from sqlalchemy.orm import sessionmaker
from models import User

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

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
