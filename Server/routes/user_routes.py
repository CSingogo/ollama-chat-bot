from services.user_service import get_users_service
from models.user_model import UserRead
from database import SessionDep
from fastapi import APIRouter, status



router = APIRouter(prefix="/users", tags=["users"])



@router.get("/",
            response_model=list[UserRead],
            status_code=status.HTTP_200_OK,
            summary="Get All Users", 
         )
def getAllUsers(session: SessionDep):
    return get_users_service(session)

