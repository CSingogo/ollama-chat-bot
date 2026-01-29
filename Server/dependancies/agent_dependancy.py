# from typing import Annotated, Any
# from fastapi import Depends, Request
# from pydantic_ai import Agent

# def get_agent(request: Request)-> Agent:
#     return request.app.state.system_agent

# Agent_Dep = Annotated[Agent, Depends(get_agent)]

# dependancies/agent_dependancy.py
from typing import Annotated
from fastapi import Depends, WebSocket, Request
from pydantic_ai import Agent

def get_agent(request: Request) -> Agent:
    """Get agent from HTTP request context"""
    return request.app.state.system_agent

def get_agent_ws(websocket: WebSocket) -> Agent:
    """Get agent from WebSocket context"""
    return websocket.app.state.system_agent

# For HTTP endpoints
Agent_Dep = Annotated[Agent, Depends(get_agent)]

# For WebSocket endpoints
Agent_Dep_WS = Annotated[Agent, Depends(get_agent_ws)]