from fastapi import FastAPI
from contextlib import asynccontextmanager
from .user.router import router as user_router
from .auth.router import router as auth_router
from .core.router import router as core_router
from .user.models import Base
from .core.database import engine
from .core.exception_handler import user_not_found_handler, duplicate_username_handler, incorrect_password_handler
from .user.exceptions import UserNotFoundException, DuplicateUsernameException, IncorrectPasswordException
from starlette.middleware.sessions import SessionMiddleware
import os
from redis import Redis
from authlib.integrations.starlette_client import OAuth


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("App is starting up")
    app.state.oauth = create_oauth()
    app.state.redis = init_redis()
    Base.metadata.create_all(bind=engine)
    yield
    app.state.redis.close()
    print("App is shutting down")

def init_redis() -> Redis:
    redis_url = os.environ['REDIS_URL']
    redis_client = Redis.from_url(redis_url, decode_responses=True)
    return redis_client

def create_oauth() -> OAuth:
    oauth = OAuth()
    oauth.register(
        name="google",
        client_id=os.environ["GOOGLE_CLIENT_ID"],
        client_secret=os.environ["GOOGLE_CLIENT_SECRET"],
        server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
        client_kwargs={"scope": "openid email profile"},
    )
    return oauth

app = FastAPI(lifespan=lifespan)

session_secret = os.environ['SESSION_SECRET']
app.add_middleware(SessionMiddleware, session_secret)
    
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(core_router)

app.add_exception_handler(UserNotFoundException, user_not_found_handler)
app.add_exception_handler(DuplicateUsernameException, duplicate_username_handler)
app.add_exception_handler(IncorrectPasswordException, incorrect_password_handler)
