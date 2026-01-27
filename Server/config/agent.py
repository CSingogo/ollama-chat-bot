from typing import Annotated
from models.agent_model import SupportDependencies, SupportResult
from config.settings import settings
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider
from fastapi import Depends
from fastapi.requests import HTTPConnection


provider = GoogleProvider(api_key='AIzaSyDQ6C5GEHwfgoZGBKhuamuajwHJhmINx2Y')
model = GoogleModel('gemini-2.5-flash', provider=provider)


my_agent = Agent(model,
                name=settings.project_name,
              deps_type=SupportDependencies,
            output_type=SupportResult,
              system_prompt=(
                  "You are a Genral agent. Help users with their queries"
                 "be helpfull"
              )
              )


# @my_agent.system_prompt
# def add_user_name(ctx: RunContext[SupportDependencies]) -> str:
#     return  f"User ID: {ctx.deps.user.id}"
    


# @my_agent.tool
# def get_account_status(ctx: RunContext[SupportDependencies]) -> str:
#     """Get the current user's account status."""
#     return "Active"

@my_agent.tool
async def get_isFirstPrompt(ctx: RunContext[SupportDependencies]) -> bool:
    """Get the current user's subscription plan."""
    return ctx.deps.user.isFirstprompt

# @my_agent.tool_plain
# def get_current_date() -> str:
#     """Get the current date. Use this whenever the user asks for the date."""
#     return str(date.today())



def get_agent(conn: HTTPConnection) -> Agent:
    return conn.app.state.system_agent

Agent_Dep = Annotated[Agent, Depends(get_agent)]







