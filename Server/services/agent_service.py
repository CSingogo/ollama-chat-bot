from models.user_model import UserObject
from models.agent_model import SupportDependencies
from models.chat_memory_model import ChatMemory
from config.agent import my_agent


async def chat_with_bot(user_dto: UserObject, user_message: str, redis:ChatMemory)-> dict:
    # 1. Pull previous messages from Redis
    
    history = redis.get_history(user_dto.id)
    
    # 2. Add the NEW user message to Redis immediately
    redis.add_message(user_dto.id, "user", user_message)
    
    # 3. Run the agent
    # Note: PydanticAI takes message_history in its .run() method
    result =await  my_agent.run(
        user_message, 
        deps=SupportDependencies(
            UserObject(
                id=user_dto.id,
                is_active=user_dto.is_active,
                name=user_dto.name,
                username=user_dto.username,
                account_status=user_dto.account_status,
                subscription_plan=user_dto.subscription_plan

            )
        ),
        message_history=history  # This gives the bot context!
    )
    if result:
        result_dict = result.output.model_dump()
        
        # 4. Save the Agent's response to Redis for the next turn
        redis.add_message(user_dto.id, "assistant", result_dict)
        
        return {"response": result_dict}
    return {
        'message' : "something went wrong"
    }