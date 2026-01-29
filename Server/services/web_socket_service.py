from fastapi import WebSocket, WebSocketDisconnect, status
from pydantic_ai import Agent
from pydantic_ai.messages import ModelMessage

async def chat_ws(ws: WebSocket, agent: Agent):
    await ws.accept()
    await ws.send_text('How Can I Help You Today!')
    # Initialize message history for this WebSocket connection
    message_history: list[ModelMessage] = []
    
    try:
        while True:
            prompt = await ws.receive_text()
            # prompt = await ws.receive_json()
           
            await ws.send_json({"type": "thinking"})
            
            # Pass and update message history
            message_history = await process_prompt(
                prompt=prompt,
                agent=agent,
                ws=ws,
                message_history=message_history
            )
    except WebSocketDisconnect as exc:
        print(f"Client disconnected, code={exc.code}, reason='{exc.reason}'")
    except Exception as e:
        await process_exception(e, ws)


async def process_prompt(
    *,
    prompt: str,
    agent: Agent,
    ws: WebSocket,
    message_history: list[ModelMessage]
) -> list[ModelMessage]:
    """Process prompt and return updated message history"""
    
    async with agent.run_stream(
        prompt, 
        message_history=message_history,
        deps=None  
    ) as result:
        output = await result.get_output()
        
        await ws.send_json({
            "type": "final",
            "data": output.model_dump()
        })
        
        return result.all_messages()


async def process_exception(e: Exception, ws: WebSocket):
    await ws.send_json({
        "type": "error",
        "message": str(e)
    })
    await ws.close(code=status.WS_1008_POLICY_VIOLATION)