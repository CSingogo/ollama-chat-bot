from models.user_model import (
      User,
      UserLogin,
      UserRegister
)

from utils.security import (
      hash_password,
      verify_password,
      create_access_token
)
from fastapi import HTTPException, status
from sqlmodel import  select,  Session



def login(user_login_dto: UserLogin, session: Session) -> str:
   
    user = session.exec(select(User).where(User.username == user_login_dto.username)).first()
    

    if not user or not verify_password(user_login_dto.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )


    access_token = create_access_token(data={ "sub": str(user.id),"email": user.email,
                                             "username":user.username,
                                             "account_status": user.account_status,
                                             "subscription_plan": user.subscription_plan })

 
    return access_token

def get_user_by_username(session: Session, username: str) -> bool:
   if user := session.exec(select(User).where(User.username == username)).first():
         return True
   return False


def register_user(user_reg_dto: UserRegister, session: Session) -> User:

    if  get_user_by_username(session=session,username=user_reg_dto.username ):
          raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User Already Exists",
        )
    
    if user_reg_dto.confirm_password != user_reg_dto.password:
                  raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords Dont Match",
        )
    
    hashed_pw = hash_password(user_reg_dto.password)

    new_user = User(
          name=user_reg_dto.name,
          password=hashed_pw,
          username=user_reg_dto.username
          )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user




    


      