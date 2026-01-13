from sqlmodel import SQLModel, Field

class UserBase(SQLModel):
    is_active: bool = True

class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    account_status: str
    subscription_plan: str