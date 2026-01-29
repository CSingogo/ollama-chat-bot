from sqlmodel import Relationship, SQLModel, Field
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.conversation_model import Conversation

class UserBase(SQLModel):
    is_active: bool = True

class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    password:str
    username: str = Field(index=True, unique=True)
    account_status: str = Field(default="Active")
    is_deleted: bool = Field(default=False, index=True)
    deleted_at: datetime | None = None
    subscription_plan: str = Field(default="Free Plan")
    conversations: list["Conversation"] = Relationship(back_populates="user")



class UserRegister(UserBase):
    name: str
    password:str
    username: str
    confirm_password: str

class UserLogin(UserBase):
    password:str
    username: str

class UserRead(UserBase):
    id: int 

class UserObject(UserBase):
    id: int | None = Field(default=None, primary_key=True)
    name: str | None
    username: str | None
    account_status: str = Field(default="Active")
    subscription_plan: str = Field(default="Free Plan")
    prompt: str | None
    isFirstprompt: bool = Field(default=True)