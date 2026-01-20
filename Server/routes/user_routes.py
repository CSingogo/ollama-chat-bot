from utils.security import verify_token
from services.user_service import get_users_service
from models.user_model import UserObject
from config.database import SessionDep
from fastapi import APIRouter, status, Depends



router = APIRouter(prefix="/users", tags=["users"])



@router.get("/",
            response_model=list[UserObject],
            status_code=status.HTTP_200_OK,
            summary="Get All Users", 
            dependencies=[Depends(verify_token)]
         )
def getAllUsers(session: SessionDep):
    return get_users_service(session)

