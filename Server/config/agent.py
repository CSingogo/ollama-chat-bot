import redis
from models.agent_model import SupportDependencies, SupportResult
from config.settings import settings
from utils.security import verify_token
from models.chat_memory_model import ChatMemory
from pydantic_ai import Agent, RunContext
from dotenv import load_dotenv
from models.user_model import User
from sqlmodel import(
    SQLModel,
    Field, 
    Session
)
from dataclasses import dataclass
from config.database import SessionLocal
from models.user_model import User
from contextlib import contextmanager
from typing import Annotated
from fastapi import(
     Depends,
     APIRouter,
     status
)
from datetime import date


load_dotenv() 


my_agent = Agent('groq:llama-3.3-70b-versatile',
                name=settings.project_name,
              deps_type=SupportDependencies,
             output_type=SupportResult,
              system_prompt=(
                  "You are a SaaS support agent. Help users with their queries"
                 "be helpfull"
              )
              )


@my_agent.system_prompt
def add_user_name(ctx: RunContext[SupportDependencies]) -> str:
    return  f"User ID: {ctx.deps.user.id}"
    


@my_agent.tool
def get_account_status(ctx: RunContext[SupportDependencies]) -> str:
    """Get the current user's account status."""
    return "Active"

@my_agent.tool
async def get_subscription_plan(ctx: RunContext[SupportDependencies]) -> str:
    """Get the current user's subscription plan."""
    return "Premium"

@my_agent.tool_plain
def get_current_date() -> str:
    """Get the current date. Use this whenever the user asks for the date."""
    return str(date.today())






