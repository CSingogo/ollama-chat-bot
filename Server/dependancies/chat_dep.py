
from typing import Annotated
from fastapi import Depends, Request
from models.chat_memory_model import ChatMemory


def get_chat_memory(request: Request) -> ChatMemory:
    return request.app.state.chat_memory

ChatMemoryDep = Annotated[ChatMemory , Depends(get_chat_memory)]