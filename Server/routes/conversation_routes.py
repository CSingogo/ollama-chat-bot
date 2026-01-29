# routes/conversation_routes.py
from fastapi import APIRouter, status, Depends, HTTPException
from dependancies.current_user_dependancy import get_current_user
from config.database import SessionDep
from utils.security import verify_token
# from utils.current_user import get_current_user
from models.user_model import UserObject
from models.conversation_model import (
    ConversationCreate, 
    ConversationRead, 
    ConversationReadWithMessages
)
from services.conversation_service import (
    create_conversation_service,
    get_user_conversations_service,
    get_conversation_by_id_service,
    update_conversation_title_service,
    delete_conversation_service
)

router = APIRouter(prefix="/conversations", tags=["conversations"])

@router.post("/",
            response_model=ConversationRead,
            status_code=status.HTTP_201_CREATED,
            summary="Create a new conversation",
            dependencies=[Depends(verify_token)])
def create_conversation(
    conversation: ConversationCreate,
    session: SessionDep,
    current_user: UserObject = Depends(get_current_user)
):
    """Create a new conversation for the current user"""
    return create_conversation_service(session, current_user.id, conversation)


@router.get("/",
           response_model=list[ConversationRead],
           status_code=status.HTTP_200_OK,
           summary="Get all user conversations",
           dependencies=[Depends(verify_token)])
def get_user_conversations(
    session: SessionDep,
    current_user: UserObject = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100
):
    """Get all conversations for the current user"""
    return get_user_conversations_service(session, current_user.id, skip, limit)


@router.get("/{conversation_id}",
           response_model=ConversationReadWithMessages,
           status_code=status.HTTP_200_OK,
           summary="Get conversation with messages",
           dependencies=[Depends(verify_token)])
def get_conversation_by_id(
    conversation_id: int,
    session: SessionDep,
    current_user: UserObject = Depends(get_current_user)
):
    """Get a specific conversation with all its messages"""
    return get_conversation_by_id_service(session, conversation_id, current_user.id)


@router.patch("/{conversation_id}",
             response_model=ConversationRead,
             status_code=status.HTTP_200_OK,
             summary="Update conversation title",
             dependencies=[Depends(verify_token)])
def update_conversation_title(
    conversation_id: int,
    title: str,
    session: SessionDep,
    current_user: UserObject = Depends(get_current_user)
):
    """Update the title of a conversation"""
    return update_conversation_title_service(session, conversation_id, current_user.id, title)


@router.delete("/{conversation_id}",
              status_code=status.HTTP_204_NO_CONTENT,
              summary="Delete a conversation",
              dependencies=[Depends(verify_token)])
def delete_conversation(
    conversation_id: int,
    session: SessionDep,
    current_user: UserObject = Depends(get_current_user)
):
    """Delete a conversation and all its messages"""
    delete_conversation_service(session, conversation_id, current_user.id)