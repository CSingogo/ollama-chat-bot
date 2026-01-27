from sqlmodel import SQLModel, Field

class UserBase(SQLModel):
    is_active: bool = True

class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    password:str
    username: str
    account_status: str = Field(default="Active")
    subscription_plan: str = Field(default="Free Plan")


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