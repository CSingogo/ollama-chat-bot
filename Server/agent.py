from pydantic_ai import Agent, RunContext
from dotenv import load_dotenv
from models import User
from sqlmodel import SQLModel, Field,  Session
from dataclasses import dataclass
from database import SessionLocal
from models import User
from contextlib import contextmanager
from typing import Annotated
from fastapi import Depends
from fastapi import APIRouter

load_dotenv() 


router = APIRouter(prefix="/agent", tags=["agent"])
@contextmanager
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

class DatabaseConn:
    @classmethod
    async def user_name(cls, *, id:int) -> str | None:
        with get_session() as session:
            user = session.query(User).filter_by(id=id).first()
            return user.name if user else None
        
    @classmethod
    async def account_status(cls, *, id:int) -> str:
        with get_session() as session:
            user = session.query(User).filter_by(id=id).first()
            return user.account_status if user else "Locked"
        
    @classmethod
    async def subscription_plan(cls, *, id:int) -> str:
        with get_session() as session:
            user = session.query(User).filter_by(id=id).first()
            return user.subscription_plan if user else "Free Plan"
        
@dataclass
class SupportDependencies:
    user_id: int
    db: DatabaseConn

class SupportResult(SQLModel):
    support_advice: str = Field(description="Advice returned to the user")
    escalate_to_admin: bool = Field(description="Wheather to escalate the query to an admin")
    risk_level: int = Field(description="Risk level of the query", ge=0, le=10)


my_agent = Agent('groq:llama-3.3-70b-versatile',
              deps_type=SupportDependencies,
             #implement result type
             output_type=SupportResult,
              system_prompt=(
                  "you are a Saas support agent, Help users with their accounts,"
                  "check subscription plans, and determine if their query should be escalated to an admin."
              )
              )

@my_agent.system_prompt
async def add_user_name(ctx: RunContext[SupportDependencies])-> str:
    user_name = await ctx.deps.db.user_name(id=ctx.deps.user_id)
    return f"The user's name is {user_name!r}"


@my_agent.tool
async def get_account_status(ctx: RunContext[SupportDependencies]) -> str:
    """Get the current user's account status."""
    status = await ctx.deps.db.account_status(id=ctx.deps.user_id)
    return f"Account status: {status}"

@my_agent.tool
async def get_subscription_plan(ctx: RunContext[SupportDependencies]) -> str:
    """Get the current user's subscription plan."""
    plan = await ctx.deps.db.subscription_plan(id=ctx.deps.user_id)
    return f"Subscription plan: {plan}"

AgentDep = Annotated[Agent, Depends(my_agent)]
SessionDep = Annotated[Session, Depends(get_session)]
# result = my_agent.run_sync("i have been hacked", deps=SupportDependencies(user_id=2, db=DatabaseConn()))
# print(result.output)
@router.get("/")
def ask()-> dict:
    result = my_agent.run_sync("i have been hacked", deps=SupportDependencies(user_id=2, db=DatabaseConn()))
    print(result.output)
    return {"data": f'{result.output}'}

