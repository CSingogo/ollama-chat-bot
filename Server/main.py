from typing import Annotated
from fastapi import(
     FastAPI,
     HTTPException,
     Depends,
     Request,
      Header,
      HTTPException
)
from fastapi.responses import JSONResponse
import uvicorn 
from contextlib import asynccontextmanager
from models.chat_memory_model import ChatMemory
from config.settings import settings
from utils.security import verify_token
from routes.agent_routes import router as agent_router
from routes.auth_routes import router as auth_router
from routes.user_routes import router as user_router
from contextlib import contextmanager
from config.database import SessionLocal, create_db_and_tables
from core.logging import LOGGING_CONFIG, logger
import redis
from dotenv import load_dotenv
import os



SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
loaded = False

@contextmanager
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def on_startup()-> None:
    logger.info("🚀 FastAPI application started")
    create_db_and_tables()
    load_dotenv()
       


def redis_init(app: FastAPI) -> None:
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    app.state.redis = r
    app.state.chat_memory = ChatMemory(app.state.redis)
    try:
        r.set("test_key", "It works!")
        logger.info(f"Redis says: {r.get('test_key')}")
    except Exception as e:
        logger.info(f"Connection failed: {e}")


async def shutdown_event():
    logger.info("Gracefully Shutting Down...🔻")

@asynccontextmanager
async def lifespan(app: FastAPI):
    on_startup()
    redis_init(app=app)
  
    yield
    await shutdown_event()
   



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

@app.middleware("http")
async def log_requests(request: Request, call_next):
    response = await call_next(request)

    logger.info(
        f"REQUEST BODY -> {request.body}"
    )

    return response

app.include_router(agent_router)
app.include_router(auth_router)
app.include_router(user_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True, log_config=LOGGING_CONFIG,)