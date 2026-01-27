from dataclasses import dataclass
from pydantic import Field
from sqlmodel import SQLModel
from models.user_model import UserObject

 
    
@dataclass
class SupportDependencies:
    user: UserObject
    

class SupportResult(SQLModel):
    support_advice: str = Field(description="Advice returned to the user")
    first_run: bool = Field(default=True)