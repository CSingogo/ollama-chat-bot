from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, timezone
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.user_model import User

class Conversation(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    title: str | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    messages: list["Message"] = Relationship(back_populates="conversation")
    user: "User" = Relationship(back_populates="conversations")


class ConversationCreate(SQLModel):
    title: str | None = None

class ConversationRead(SQLModel):
    id: int
    title: str | None
    created_at: datetime

class ConversationReadWithMessages(SQLModel):
    id: int
    title: str | None
    created_at: datetime
    messages: list["MessageRead"]


class MessageBase(SQLModel):
     pass

class Message(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    conversation_id: int = Field(foreign_key="conversation.id", index=True)
    user_id: int = Field(foreign_key="user.id", index=True)

    role: str  # "user" | "assistant" | "system"
    content: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    conversation: Conversation = Relationship(back_populates="messages")


class MessageCreate(SQLModel):
    content: str

class MessageRead(SQLModel):
    id: int
    role: str
    content: str
    created_at: datetime



