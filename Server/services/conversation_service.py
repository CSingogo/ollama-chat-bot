# services/conversation_service.py
from sqlmodel import Session, select
from fastapi import HTTPException, status
from models.conversation_model import (
    Conversation, 
    ConversationCreate, 
    ConversationRead,
    ConversationReadWithMessages
)
from models.user_model import User


def create_conversation_service(
    session: Session, 
    user_id: int, 
    conversation: ConversationCreate
) -> Conversation:
    """Create a new conversation"""
    # Verify user exists
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    new_conversation = Conversation(
        user_id=user_id,
        title=conversation.title or "New Conversation"
    )
    session.add(new_conversation)
    session.commit()
    session.refresh(new_conversation)
    return new_conversation


def get_user_conversations_service(
    session: Session, 
    user_id: int, 
    skip: int = 0, 
    limit: int = 100
) -> list[Conversation]:
    """Get all conversations for a user"""
    statement = (
        select(Conversation)
        .where(Conversation.user_id == user_id)
        .order_by(Conversation.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    conversations = session.exec(statement).all()
    return list(conversations)


def get_conversation_by_id_service(
    session: Session, 
    conversation_id: int, 
    user_id: int
) -> Conversation:
    """Get a specific conversation with messages"""
    conversation = session.get(Conversation, conversation_id)
    
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    if conversation.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this conversation"
        )
    
    return conversation


def update_conversation_title_service(
    session: Session, 
    conversation_id: int, 
    user_id: int, 
    title: str
) -> Conversation:
    """Update conversation title"""
    conversation = session.get(Conversation, conversation_id)
    
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    if conversation.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this conversation"
        )
    
    conversation.title = title
    session.add(conversation)
    session.commit()
    session.refresh(conversation)
    return conversation


def delete_conversation_service(
    session: Session, 
    conversation_id: int, 
    user_id: int
) -> None:
    """Delete a conversation and all its messages"""
    conversation = session.get(Conversation, conversation_id)
    
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    if conversation.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this conversation"
        )
    
    session.delete(conversation)
    session.commit()