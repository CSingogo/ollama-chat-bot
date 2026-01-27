from fastapi import APIRouter, WebSocket, Depends
from config.agent import  Agent_Dep
from services.web_socket_service import chat_ws

ws_router = APIRouter(prefix="/chat_ws", tags=["WS"])

@ws_router.websocket("/")
async def post_message(ws:WebSocket, agent: Agent_Dep):
    return await chat_ws(ws,agent=agent)





