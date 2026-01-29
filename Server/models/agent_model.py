from dataclasses import dataclass
from pydantic import Field
from sqlmodel import SQLModel
from models.user_model import UserObject

 
    
@dataclass
class SupportDependencies:
    user: UserObject
    

class SupportResult(SQLModel):
    advice: str = Field(description="Advice returned to the user")