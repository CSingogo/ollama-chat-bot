# routes/message_routes.py
from fastapi import APIRouter, status, Depends
from dependancies.current_user_dependancy import get_current_user
from config.database import SessionDep
from utils.security import verify_token
from models.user_model import UserObject
from models.conversation_model import MessageCreate, MessageRead
from services.message_service import (
    create_message_service,
    get_conversation_messages_service
)

router = APIRouter(prefix="/messages", tags=["messages"])

@router.post("/conversations/{conversation_id}",
            response_model=MessageRead,
            status_code=status.HTTP_201_CREATED,
            summary="Add message to conversation",
            dependencies=[Depends(verify_token)])
def create_message(
    conversation_id: int,
    message: MessageCreate,
    session: SessionDep,
    current_user: UserObject = Depends(get_current_user),
    role: str = "user"  # Can be "user" or "assistant"
):
    """Add a new message to a conversation"""
    return create_message_service(
        session, 
        conversation_id, 
        current_user.id, 
        message, 
        role
    )


@router.get("/conversations/{conversation_id}",
           response_model=list[MessageRead],
           status_code=status.HTTP_200_OK,
           summary="Get conversation messages",
           dependencies=[Depends(verify_token)])
def get_conversation_messages(
    conversation_id: int,
    session: SessionDep,
    current_user: UserObject = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100
):
    """Get all messages for a specific conversation"""
    return get_conversation_messages_service(
        session, 
        conversation_id, 
        current_user.id, 
        skip, 
        limit
    )