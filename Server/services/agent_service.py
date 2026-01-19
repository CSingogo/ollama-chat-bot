from models.agent_model import SupportDependencies
from models.chat_memory_model import ChatMemory
from config.agent import my_agent


async def chat_with_bot(user_id: int, user_message: str, r:ChatMemory)-> dict:
    # 1. Pull previous messages from Redis
    
    history = r.get_history(user_id)
    
    # 2. Add the NEW user message to Redis immediately
    r.add_message(user_id, "user", user_message)
    
    # 3. Run the agent
    # Note: PydanticAI takes message_history in its .run() method
    result =await  my_agent.run(
        user_message, 
        deps=SupportDependencies(user_id=user_id, user_info={
        "USER_ID" : 1,
        "AGE": 24
   }),
        message_history=history  # This gives the bot context!
    )
    if result:
        result_dict = result.output.model_dump()
        
        # 4. Save the Agent's response to Redis for the next turn
        r.add_message(user_id, "assistant", result_dict)
        
        return {"response": result_dict}
    return {
        'message' : "something went wrong"
    }