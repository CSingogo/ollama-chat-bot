from typing import Annotated, Any
from fastapi import Depends, Request
from pydantic_ai import Agent

def get_agent(request: Request)-> Agent:
    return request.app.state.system_agent

Agent_Dep = Annotated[Any, Depends(get_agent)]