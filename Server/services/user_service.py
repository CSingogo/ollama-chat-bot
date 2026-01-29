from models.user_model import User, UserObject
from sqlmodel import  select, Session


def get_users_service(session: Session) -> list[UserObject]: # type: ignore
    users =  session.exec(select(User)).all()
    return users

def get_user_by_id(session: Session, user_id: int):
    user = session.exec(select(User).where(User.id == user_id))
    return user

