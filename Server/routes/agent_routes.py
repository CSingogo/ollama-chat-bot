from fastapi import APIRouter, Depends, status
from dependancies.chat_dep import ChatMemoryDep
from services.agent_service import chat_with_bot
from utils.security import verify_token


router = APIRouter(prefix="/agent", tags=["agent"])

# @router.post("/")
# def ask()-> dict:
#     result = my_agent.run_sync("i have been hacked", deps=SupportDependencies(user_id=1, db=DatabaseConn(), ),)
#     print(result.output)
#     return {"data": f'{result.output}'}

# r = RedisDep
# memory = ChatMemory(r)

@router.post("/chat/{user_id}",
    
            status_code=status.HTTP_201_CREATED,
            summary="Post A Message", 
            description="Creates A New User Message, And Sends To Chat Bot",
            response_description="A Dict With THe Response",
            dependencies=[Depends(verify_token)]
            )
def chat_with_bot_route(user_id: int,  user_message: str, redis:ChatMemoryDep):
    return chat_with_bot(user_id=user_id, user_message=user_message, redis=redis)