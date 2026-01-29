from fastapi import APIRouter, WebSocket, Depends
from pydantic_ai import Agent
from dependancies.agent_dependancy import Agent_Dep_WS
from services.web_socket_service import chat_ws

ws_router = APIRouter(prefix="/chat_ws", tags=["WS"])

@ws_router.websocket("/")
async def post_message(ws:WebSocket, agent: Agent_Dep_WS):
    return await chat_ws(ws,agent=agent)





