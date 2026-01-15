from models.user_model import User, UserRead
from sqlmodel import  select, Session


def get_users_service(session: Session) -> list[UserRead]: # type: ignore
    users =  session.exec(select(User)).all()
    return users