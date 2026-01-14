from fastapi import FastAPI, HTTPException, Depends
import uvicorn 
from agent import my_agent, DatabaseConn , SupportDependencies
from typing import Annotated
from pydantic_ai import Agent
from agent import router as agent_router


app = FastAPI(title="Chat App")
app.include_router(agent_router)
items = {"foo": "The Foo Wrestlers"}


def get_agent() -> Agent:
    return my_agent

AgentDep = Annotated[Agent, Depends(get_agent)]

@app.get("/items/{item_id}")
async def read_item(item_id: str):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item": items[item_id]}

# @app.get("/agent")
# async def request(agent : AgentDep)-> dict:
#     result = agent.run_sync("i have been hacked", deps=SupportDependencies(user_id=2, db=DatabaseConn()))
#     print(result.output)
#     return {"agent" : f"{result.output}"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)