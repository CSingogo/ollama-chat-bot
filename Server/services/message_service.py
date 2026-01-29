# services/message_service.py
from sqlmodel import Session, select
from fastapi import HTTPException, status
from models.conversation_model import (
    Message, 
    MessageCreate, 
    Conversation
)


def create_message_service(
    session: Session,
    conversation_id: int,
    user_id: int,
    message: MessageCreate,
    role: str = "user"
) -> Message:
    """Create a new message in a conversation"""
    # Verify conversation exists and belongs to user
    conversation = session.get(Conversation, conversation_id)
    
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    if conversation.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to add messages to this conversation"
        )
    
    new_message = Message(
        conversation_id=conversation_id,
        user_id=user_id,
        role=role,
        content=message.content
    )
    
    session.add(new_message)
    session.commit()
    session.refresh(new_message)
    return new_message


def get_conversation_messages_service(
    session: Session,
    conversation_id: int,
    user_id: int,
    skip: int = 0,
    limit: int = 100
) -> list[Message]:
    """Get all messages for a conversation"""
    # Verify conversation belongs to user
    conversation = session.get(Conversation, conversation_id)
    
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    if conversation.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view messages in this conversation"
        )
    
    statement = (
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.asc())
        .offset(skip)
        .limit(limit)
    )
    messages = session.exec(statement).all()
    return list(messages)