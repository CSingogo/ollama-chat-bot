
from services.auth_service import login, register_user
from Server.config.database import SessionDep
from models.user_model import UserLogin, UserRead, UserRegister
from fastapi import APIRouter, status


router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/login", status_code=status.HTTP_200_OK)
def auth_login(loginDto: UserLogin, session: SessionDep):
    return login(loginDto, session)

@router.post("/register",
             response_model=UserRead,
             status_code=status.HTTP_201_CREATED,
            summary="Register a new user", 
            description="Creates a new user in the database and hashes their password.",
            response_description="The newly created user profile")
def auth_register(createUserDto: UserRegister, session: SessionDep):
    return register_user(createUserDto, session)