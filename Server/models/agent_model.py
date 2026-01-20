from dataclasses import dataclass
from pydantic import Field
from sqlmodel import SQLModel
from models.user_model import UserObject
import redis

 
    
@dataclass
class SupportDependencies:
    user: UserObject
    # redis: redis.Redis
    

class SupportResult(SQLModel):
    support_advice: str = Field(description="Advice returned to the user")
    escalate_to_admin: bool = Field(description="Wheather to escalate the query to an admin")
    risk_level: int = Field(description="Risk level of the query", ge=0, le=10)