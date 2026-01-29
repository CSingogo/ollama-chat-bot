from fastapi import(
     FastAPI,
     Request,
)
from fastapi.responses import JSONResponse
import uvicorn 
from contextlib import asynccontextmanager
from config.settings import settings
from routes.auth_routes import router as auth_router
from routes.user_routes import router as user_router
from routes.chat_web_socket_routes import ws_router 
from routes.conversation_routes import router as conversation_router
from routes.message_routes import router as message_router
from contextlib import contextmanager
from config.database import SessionLocal, create_db_and_tables
from core.logging import LOGGING_CONFIG, logger
from dotenv import load_dotenv
from config.agent import my_agent_instance



@contextmanager
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
  
    logger.info("🚀 FastAPI application started")
    create_db_and_tables()
    load_dotenv()
    app.state.system_agent = my_agent_instance.my_agent
    yield
    logger.info("Gracefully Shutting Down...🔻")
   



app = FastAPI(title=settings.project_name,
              version=settings.version, 
              summary="A Cool Chatbot App",
              lifespan=lifespan,
             )

@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={"error": str(exc)}
    )


# app.include_router(agent_router)
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(ws_router)
app.include_router(conversation_router)
app.include_router(message_router)



if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True, log_config=LOGGING_CONFIG,)