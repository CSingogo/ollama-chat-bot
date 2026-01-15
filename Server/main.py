from fastapi import FastAPI, HTTPException, Depends
import uvicorn 
from core.agent import my_agent, DatabaseConn , SupportDependencies
from typing import Annotated
from pydantic_ai import Agent
from core.agent import router as agent_router
from routes.auth_routes import router as auth_router
from routes.user_routes import router as user_router
from contextlib import contextmanager
from database import SessionLocal, create_db_and_tables
from core.logging import LOGGING_CONFIG, logger



app = FastAPI(title="Chat App", version="0.1.0")


@contextmanager
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

@app.on_event("startup")
def on_startup():
    logger.info("🚀 FastAPI application started")
    create_db_and_tables()

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Gracefully Shutting Down...")



app.include_router(agent_router)
app.include_router(auth_router)
app.include_router(user_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True, log_config=LOGGING_CONFIG,)